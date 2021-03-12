from django.shortcuts import render, redirect
import requests, json
from django.contrib.auth.models import User
from users.models import Profile
from newsapi import NewsApiClient
import tweepy as tw
import datetime
from theguardian import theguardian_content
from theguardian import theguardian_tag


rapid_api_headers = {
    'x-rapidapi-key': "0d18a23271msh79f81ab985ee668p136a4ajsnac5b16b6c7cc",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

news_api = NewsApiClient(api_key='50739f8214614b9f944e58c8d8209288')

TWITTER_API_KEY = 'r0FBVnOkwRurF0tTF34hhyTxh'
TWITTER_API_KEY_SECRET = '22IQVnbXlRoTsCqGDqUwfgH7zb5xizWChYFnnEUMBCTzXok3Be'
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAALW0KgEAAAAAAOWQDB%2FgpcTjiJqAJMA8KOQ2ZSY%3D3L108RpgkPU5BtoP1relmzRRNSOCxWbVNhySL13OuS7jumXXH8'
TWITTER_ACCESS_TOKEN = '1182607642172235776-gTee9y22mcd1v84se20QfdlOPizgeB'
TWITTER_ACCESS_TOKEN_SECRET = 'QmGHIkvSxb2myUvRLEuBiRn5ACMUfcjpjZXkxipLqWf0U'

auth = tw.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

guardian_api_key = "4a293514-81cc-43db-b1d1-d0ca39863424"


def get_premier_league_teams():
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/2790"
    response = requests.request("GET", url, headers=rapid_api_headers)
    return json.loads(response.text)['api']['teams']


def get_team_details(team_id):
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/team/" + str(team_id)
    response = requests.request("GET", url, headers=rapid_api_headers)
    return json.loads(response.text)['api']['teams'][0]


def get_team_results(team_id, amount):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/" + str(team_id) + "/last/" + str(amount)
    response = requests.request("GET", url, headers=rapid_api_headers)
    return json.loads(response.text)['api']['fixtures']


def get_team_tweets(team_name, amount):
    team_tweets = [t for t in tw.Cursor(api.search,
        q=team_name, count=10, lang="en", result_type="mixed").items(amount)]
    return team_tweets


def get_team_news(team_name, page_number, page_size):
    news = news_api.get_top_headlines(
        q = team_name,
        category = "sports",
        language = 'en',
        page_size = page_size,
        page = page_number
    )
    return news


# pages of 10 articles
def get_guardian_articles(team_name, page_number):
    # get team's tag api URL
    headers = {
        "q": team_name,
        "section": "football",
        "show-references": "all",
    }
    tag = theguardian_tag.Tag(guardian_api_key, **headers)
    tag_content = tag.get_content_response()
    print(tag_content)
    results = tag.get_results(tag_content)
    tag_api_url = results[0]["apiUrl"]
    # get articles from tag
    content = theguardian_content.Content(
        guardian_api_key,
        url = tag_api_url,
        page = page_number)
    content_response = content.get_content_response()
    return content_response['response']['results']


def get_feed(followed_teams, posts_per_team):
    news_api_articles = []
    guardian_articles = []
    for team in followed_teams:
        response = get_team_news(team.name)
        news_api_articles += response['articles']
        response = get_guardian_articles(team.name)
        guardian_articles += response
    for article in guardian_articles:
        article['publishedAt'] = article['webPublicationDate']
        del article['webPublicationDate']
        article['title'] = article['webTitle']
        del article['webTitle']
        article['url'] = article['webUrl']
        del article['webUrl']
        article['source'] = "The Guardian"
    for article in news_api_articles:
        source_name = article['source']['name']
        article['source'] = source_name
    articles = news_api_articles + guardian_articles
    # bubble sort by date
    l = len(articles)
    for n in range(l):
        for k in range(0, l-n-1):
            if get_article_date(articles[k]) < get_article_date(articles[k+1]):
                articles[k], articles[k+1] = articles[k+1], articles[k]
    # remove copy articles
    copy_article_indexes = []
    for n in range(l-1):
        if articles[n]["title"] == articles[n+1]["title"]:
            copy_article_indexes.append(n+1)
    for index in copy_article_indexes:
        articles[index] = None
    for i in range(len(copy_article_indexes)):
        articles.remove(None)
    return articles

def get_article_date(article):
    return datetime.datetime.strptime(article['publishedAt'][:-4],"%Y-%m-%dT%H:%M")
