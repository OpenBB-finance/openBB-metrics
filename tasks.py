import json
import praw
import requests
from datetime import datetime, timedelta
from utilities.config import settings

current_date = str(datetime.utcnow().date())


def send_request(url, data=None, type_req="POST"):
    if data is None:
        data = {}
    return requests.request(type_req, f"http://127.0.0.1:8000/{url}",
                            data=json.dumps(data),
                            headers={'Content-Type': 'application/json'}).json()


def get_terminal_downloads():
    """
    Get terminal download statistics
    """
    data = requests.get("https://api.github.com/repos/OpenBB-finance/openbbterminal/releases/latest").json()
    version, macos, windows = data["tag_name"], 0, 0
    for installer in data["assets"]:
        # macOS terminal downloads
        if installer["name"].endswith(".dmg"):
            macos = installer["download_count"]

        # windows terminal downloads
        elif installer["name"].endswith(".exe"):
            windows = installer["download_count"]

    response = send_request("terminal_downloads",
                            {"tag_name": version, "macos": macos, "windows": windows, "updated_date": current_date})
    return response


def twitter_bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {settings.TWITTER_BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_twitter_endpoint(url):
    response = requests.get(url, auth=twitter_bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an errors: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_twitter_stats():
    """
    Get twitter statistics
    """
    url = "https://api.twitter.com/1.1/users/show.json?screen_name=openbb_finance"
    data = connect_to_twitter_endpoint(url)
    total_followers = data["followers_count"]

    data = send_request("twitter", type_req="GET")
    prev_followers = 0
    if data:
        if data[-1]["total_followers"] is not None:
            prev_followers = data[-1]["total_followers"]

    new_followers = total_followers - prev_followers

    url = "https://api.twitter.com/2/users/1388522440536494081/tweets?tweet.fields=attachments,author_id,created_at," \
          "public_metrics,source,referenced_tweets"
    data = connect_to_twitter_endpoint(url)
    likes, retweets = 0, 0
    for i in data["data"]:
        metrics = i["public_metrics"]
        if i["created_at"] > str(datetime.utcnow() - timedelta(days=1)):
            likes += metrics["like_count"]
            retweets += metrics["retweet_count"]

    response = send_request("twitter",
                            {"total_followers": total_followers, "new_followers": new_followers, "likes": likes,
                             "retweets": retweets, "updated_date": current_date})
    return response


def get_reddit_stats():
    """
    Get reddit statistics
    """
    reddit = praw.Reddit(client_id=settings.REDDIT_CLIENT_ID,
                         client_secret=settings.REDDIT_CLIENT_SECRET,
                         user_agent=settings.REDDIT_USER_AGENT)
    subreddit = reddit.subreddit("openBB")
    followers = subreddit.subscribers
    response = send_request("reddit", {"total_followers": followers, "updated_date": current_date})
    return response


if __name__ == '__main__':
    get_terminal_downloads()
    get_twitter_stats()
    get_reddit_stats()
