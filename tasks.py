import json
import praw
import requests
from bs4 import BeautifulSoup
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

    url = "https://api.twitter.com/2/tweets/counts/recent?query=openbb&granularity=hour"
    data = connect_to_twitter_endpoint(url)
    mentions = 0
    for i in data["data"][-24:]:
        mentions += i["tweet_count"]

    response = send_request("twitter",
                            {"total_followers": total_followers, "new_followers": new_followers, "likes": likes,
                             "retweets": retweets, "mentions": mentions, "updated_date": current_date})
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


def get_discord_stats():
    return


def get_headlines_stats():
    """
    Get news headlines statistics
    """
    url = f"https://newsapi.org/v2/everything?q=openbb&apiKey={settings.NEWSAPI_TOKEN}"
    data = requests.get(url)
    for i in data.json()["articles"]:
        response = send_request("headlines", {"source": i["source"]["name"], "title": i["title"], "url": i["url"],
                                              "published_date": i["publishedAt"]})
        print(response)


def get_youtube_stats():
    """
    Get YouTube statistics
    """
    url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=openbb&publishedAfter=2022-01-01T00%3A00" \
          f"%3A00Z&order=date&key={settings.YOUTUBE_TOKEN}"
    data = requests.get(url)
    for i in data.json()["items"]:
        response = send_request("youtube", {"channel": i["snippet"]["channelTitle"],
                                            "title": i["snippet"]["title"],
                                            "video_id": i["id"]["videoId"],
                                            "published_date": i["snippet"]["publishTime"]})
        print(response)


def get_linkedin_stats():
    x = requests.get("http://localhost:8000/linkedin").json()

    url = "https://www.linkedin.com/pages-extensions/FollowCompany?id=76491268&counter=bottom"
    data = requests.get(url)
    soup = BeautifulSoup(data.content, 'html.parser')
    followers = int(soup.select_one('.follower-count').text)

    data = send_request("linkedin", type_req="GET")
    prev_followers = 0
    if data:
        if data[-1]["total_followers"] is not None:
            prev_followers = data[-1]["total_followers"] 

    new_followers = followers - prev_followers
    response = send_request("linkedin", {"new_followers": new_followers, "total_followers": followers, "updated_date": current_date})
    return response


if __name__ == '__main__':
    get_terminal_downloads()
    get_twitter_stats()
    get_reddit_stats()
    get_discord_stats()
    get_headlines_stats()
    get_youtube_stats()
    get_linkedin_stats()
