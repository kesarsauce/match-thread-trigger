import os

reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")


espn_base_url = "https://www.espn.in/football"
isl_fixtures_url = espn_base_url + "/schedule/_/league/ind.1"
ileague_fixtures_url = espn_base_url + "/schedule/_/league/ind.2"
india_nt_fixtures_url = espn_base_url + "/team/fixtures/_/id/4385/ind"