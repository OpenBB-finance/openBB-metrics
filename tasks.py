import json
import praw
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from utilities.config import settings

# current_date = str(datetime.utcnow().date())
current_date = int(datetime.timestamp(datetime.now()))


def send_request(url, data=None, type_req="POST"):
    if data is None:
        data = {}
    return requests.request(type_req, f"http://127.0.0.1:8000/{url}",
                            data=json.dumps(data),
                            headers={'Content-Type': 'application/json'}).json()


def convert_to_timestamp(date_str):
    return int(datetime.timestamp(datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')))


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


def get_headlines_stats():
    """
    Get news headlines statistics
    """
    url = f"https://newsapi.org/v2/everything?q=openbb&apiKey={settings.NEWSAPI_TOKEN}"
    data = requests.get(url)
    for i in data.json()["articles"]:
        published_date = convert_to_timestamp(i["publishedAt"])
        response = send_request("headlines", {"source": i["source"]["name"], "title": i["title"], "url": i["url"],
                                              "published_date": published_date})
        print(response)


def get_youtube_stats():
    """
    Get YouTube statistics
    """
    url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=openbb&publishedAfter=2022-01-01T00%3A00" \
          f"%3A00Z&order=date&key={settings.YOUTUBE_TOKEN}"
    data = requests.get(url)
    for i in data.json()["items"]:
        published_date = convert_to_timestamp(i["snippet"]["publishTime"])
        response = send_request("youtube", {"channel": i["snippet"]["channelTitle"],
                                            "title": i["snippet"]["title"],
                                            "video_id": i["id"]["videoId"],
                                            "published_date": published_date})
        print(response)


def get_linkedin_stats():
    """
    Get Linkedin statistics
    """
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
    response = send_request("linkedin", {"new_followers": new_followers, "total_followers": followers,
                                         "updated_date": current_date})
    return response


def get_discord_stats():
    """
    Get Discord statistics
    """
    header = {
        "authorization": f"Bot {settings.DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }
    url = "https://discord.com/api/v7/guilds/831165782750789672?with_counts=true"
    data = requests.get(url, headers=header).json()
    total_followers = data["approximate_member_count"]
    active_followers = data["approximate_presence_count"]

    data = send_request("discord", type_req="GET")
    prev_followers = 0
    if data:
        if data[-1]["total_followers"] is not None:
            prev_followers = data[-1]["total_followers"]

    new_followers = total_followers - prev_followers

    response = send_request("discord", {"new_followers": new_followers, "total_followers": total_followers,
                                        "active_followers": active_followers, "updated_date": current_date})
    return response


def add_page_number(current_url):
    current_url, current_page_num = current_url.rsplit("=", 1)
    new_url = current_url + str(int(current_page_num) + 1)
    return new_url


def get_github_stats():
    """
    Get Github statistics
    """
    url = "https://api.github.com/repos/OpenBB-finance/OpenBBTerminal/contributors?per_page=100&anon=false&page=1"
    contributors = 0
    data = requests.get(url).json()
    contributors += len(data)
    while len(data) == 100:
        url = add_page_number(url)
        data = requests.get(url).json()
        contributors += len(data)

    url = "https://api.github.com/repos/OpenBB-finance/OpenBBTerminal"
    data = requests.get(url).json()
    stars = data["stargazers_count"]
    forks = data["forks_count"]
    total_issues_count = data["open_issues_count"]

    url = "https://api.github.com/search/issues?q=repo:OpenBB-finance/OpenBBTerminal%20is:pr%20is:open"
    data = requests.get(url).json()
    open_pr = data["total_count"]

    url = "https://api.github.com/search/issues?q=repo:OpenBB-finance/OpenBBTerminal%20is:pr%20is:closed"
    data = requests.get(url).json()
    closed_pr = data["total_count"]

    issues = total_issues_count - open_pr

    response = send_request("github", {"contributors": contributors, "stars": stars, "forks": forks,
                                       "open_pr": open_pr, "closed_pr": closed_pr, "issues": issues,
                                       "updated_date": current_date})
    return response


if __name__ == '__main__':
    get_terminal_downloads()
    get_twitter_stats()
    get_reddit_stats()
    get_discord_stats()
    get_linkedin_stats()
    get_headlines_stats()
    get_youtube_stats()
    get_github_stats()
