from datetime import datetime

from bs4 import BeautifulSoup
import requests
from flask import current_app as app

from constants import isl_fixtures_url, ileague_fixtures_url, india_nt_fixtures_url
from reddit_client import reddit


def parse_league_fixtures(league_url):
    resp = requests.get(league_url)

    html_data = resp.text
    soup = BeautifulSoup(html_data, features="html.parser")
    data = soup.select("tbody>tr")
    data = [i for i in data if 'has-results' not in i.attrs['class']]

    matchid_to_matchdate = {}

    for row in data:
        match_id_tag=row.find("td").find("span", class_="record")
        match_id = match_id_tag.a.attrs['href'].split('/')[-1]
        try:
            match_date = get_match_date(match_id)
        except Exception as e:
            continue

        if match_date.date() > datetime.utcnow().date():
            break

        matchid_to_matchdate[match_id] = match_date

    return matchid_to_matchdate

def parse_nt_fixtures():
    resp = requests.get(india_nt_fixtures_url)

    html_data = resp.text
    soup = BeautifulSoup(html_data, features="html.parser")
    data = soup.select("tbody>tr")

    matchid_to_matchdate = {}

    for row in data:
        match_id_tag = row.select("tbody>tr>td")[2].find("span").find_all("a")[1]
        match_id = match_id_tag.attrs["href"].split("/")[-1]
        try:
            match_date = get_match_date(match_id)
        except Exception as e:
            continue

        if match_date.date() > datetime.utcnow().date():
            break

        matchid_to_matchdate[match_id] = match_date

    return matchid_to_matchdate

def get_match_date(match_id) -> datetime:
    resp = requests.get(f"https://www.espn.in/football/match/_/gameId/{match_id}")

    html_data = resp.text
    soup = BeautifulSoup(html_data, features="html.parser")

    data = soup.select("div.team-info a.team-name")
    team_names = " vs ".join([team.select_one("span.long-name").text for team in data])
    try:
        match_date = soup.select_one("div.game-status").find("span").attrs["data-date"]
        match_date = datetime.strptime(match_date, "%Y-%m-%dT%H:%MZ")
        return match_date
    except KeyError:
        app.logger.warning(f"FT for selected matchid {match_id} : {team_names}")
        raise Exception

def trigger_match_thread():
    """
        - get matches for the day
        - send PMs for all matches within 1 hr kickoff
        - set cron trigger for the 1st match outside 1 hr window
    """
    matches_data = {}
    matches_data.update(
        {
            **parse_league_fixtures(isl_fixtures_url),
            **parse_league_fixtures(ileague_fixtures_url),
            **parse_nt_fixtures(),
        }
    )

    # sort ascending order by date
    match_pipeline = [dict(match_id=k, match_date=matches_data[k]) for k in sorted(matches_data, key=matches_data.get)]
    match_pipeline = [dict(match_id="54321", match_date=datetime(year=2023, month=1, day=8, hour=18, minute=50))]

    app.logger.info(f"Matches in pipeline: {len(match_pipeline)}")

    for match in match_pipeline:
        match_id = match.get("match_id")
        match_date = match.get("match_date")

        minutes_to_kickoff = (match_date - datetime.utcnow()).seconds//60
        if minutes_to_kickoff <= 60:
            app.logger.info("match kickoff within 1 hr sending PM")
            reddit.redditor("MatchThreadder").message(subject="Match Thread", message=f"{match_id} for /r/IndianFootball")
            
        else:
            app.logger.info(f"next cron trigger for match in {minutes_to_kickoff - 60} minutes")
            return {"next_cron_trigger": f"{match_date.minute} {match_date.hour-1} {match_date.day} {match_date.month} *"}

    app.logger.info("No matches today to set cron trigger for!")
    return {"next_cron_trigger": None}   
