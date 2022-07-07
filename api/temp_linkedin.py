import requests
from bs4 import BeautifulSoup

def get_linkedin_followers():
    url = 'https://www.linkedin.com/pages-extensions/FollowCompany?id=76491268&counter=bottom'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    followers = soup.select_one('.follower-count').text
    print(followers)