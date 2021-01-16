from django.shortcuts import render
import requests, json

rapid_api_headers = {
    'x-rapidapi-key': "0d18a23271msh79f81ab985ee668p136a4ajsnac5b16b6c7cc",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

def index(request):
    args = {}
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/2790"
    response = requests.request("GET", url, headers = rapid_api_headers)
    res_dict = json.loads(response.text)
    args['premier_league_teams'] = res_dict['api']['teams']
    return render(request, 'index.html', args)

