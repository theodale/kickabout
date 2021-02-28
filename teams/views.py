from django.shortcuts import render, redirect
import requests, json
from django.contrib.auth.models import User
from users.models import Profile
from .models import Team
from newsapi import NewsApiClient
import tweepy as tw
from theguardian import theguardian_content
from theguardian import theguardian_section
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
api = tw.API(auth,wait_on_rate_limit=True)

guardian_api_key = "4a293514-81cc-43db-b1d1-d0ca39863424"

def index(request):
    # get premier league teams
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/2790"
    response = requests.request("GET", url, headers = rapid_api_headers)
    res_dict = json.loads(response.text)
    if request.user.is_authenticated:
        followed_teams = [team.api_id for team in request.user.profile.teams.all()]
    else:
        followed_teams = []
    args = {
        'premier_league_teams': res_dict['api']['teams'],
        'followed_teams': followed_teams,
    }
    return render(request, 'index.html', args)

def show(request, team_id):
    # get team details
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/team/" + str(team_id)
    response = requests.request("GET", url, headers=rapid_api_headers)
    res_dict_team = json.loads(response.text)
    team_name = res_dict_team['api']['teams'][0]['name']
    args = {
        'details': res_dict_team['api']['teams'][0],
    }

    # get teams results
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/" + str(team_id) + "/last/20"
    response = requests.request("GET", url, headers=rapid_api_headers)
    res_dict_fixtures = json.loads(response.text)
    args['results'] = res_dict_fixtures['api']['fixtures']

    #get team headlines
    top_headlines = news_api.get_top_headlines(q=team_name,
                                               category = 'sports',
                                               language = 'en',
                                               country = 'gb')
    args['headlines'] = top_headlines

    #get team-related tweets
    related_tweets = [t for t in tw.Cursor(api.search,q=team_name, count=10, lang="en", result_type="mixed").items(30)]
    args['related_tweets'] = related_tweets

    # get guardian articles
    headers = {
        "q": team_name,
        "section": "football",
        "show-references": "all",
    }
    tag = theguardian_tag.Tag(api="4a293514-81cc-43db-b1d1-d0ca39863424", **headers)

    # get the results
    tag_content = tag.get_content_response()
    results = tag.get_results(tag_content)
    tag_api_url = results[0]["apiUrl"] # get tags apiUrl
    content = theguardian_content.Content(api="4a293514-81cc-43db-b1d1-d0ca39863424", url=tag_api_url)
    content_response = content.get_content_response()
    args['guardian_articles'] = content_response['response']['results']

    return render(request, 'show.html', args)

def follow_team(request, api_id, name):
    profile = request.user.profile
    try:
        team = Team.objects.get(api_id=api_id)
    except Team.DoesNotExist:
        team = Team(name=name, api_id=api_id)
        team.save()
    profile.follow_team(team)
    return redirect('/teams/')

def unfollow_team(request, api_id, name):
    profile = request.user.profile
    team = Team.objects.get(api_id=api_id)
    profile.unfollow_team(team)
    return redirect('/teams/')
