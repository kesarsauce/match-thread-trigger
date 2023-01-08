import praw

from constants import reddit_username, reddit_password, reddit_client_id, reddit_client_secret, reddit_user_agent

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent,
    password=reddit_password,
    username=reddit_username,
)