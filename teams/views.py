from django.shortcuts import render, redirect
import requests, json
from django.contrib.auth.models import User
from users.models import Profile
from .models import Team


rapid_api_headers = {
    'x-rapidapi-key': "0d18a23271msh79f81ab985ee668p136a4ajsnac5b16b6c7cc",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

def index(request):
    # get premier league teams
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/2790"
    response = requests.request("GET", url, headers = rapid_api_headers)
    res_dict = json.loads(response.text)
    args = {
        'premier_league_teams': res_dict['api']['teams'],
        'followed_teams': [team.api_id for team in request.user.profile.teams.all()],
    }
    return render(request, 'index.html', args)

def show(request, team_id):
    # get team details
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/team/" + str(team_id)
    response = requests.request("GET", url, headers=rapid_api_headers)
    res_dict_team = json.loads(response.text)
    print(res_dict_team)

    # get teams results
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/" + str(team_id) + "/last/20"
    response = requests.request("GET", url, headers=rapid_api_headers)
    res_dict_fixtures = json.loads(response.text)

    args = {
        'details': res_dict_team['api']['teams'][0],
        'fixtures': res_dict_fixtures['api']['fixtures'],
    }

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
