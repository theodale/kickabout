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
from utils.kickabout_api_manager import *

def index(request):
    if request.user.is_authenticated:
        followed_teams = [team.api_id for team in request.user.profile.teams.all()]
    else:
        followed_teams = []
    args = {
        'premier_league_teams': get_premier_league_teams(),
        'followed_teams': followed_teams,
    }
    return render(request, 'index.html', args)

def show(request, team_id):
    team_details = get_team_details(team_id)
    team_name = team_details['name']

    args = {
        'details': team_details,
        'results': get_team_results(team_id, 10),
        'headlines': get_team_news(team_name, 1, 100),
        'tweets': get_team_tweets(team_name, 10),
        'guardian_articles': get_guardian_articles(team_name, 1)
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
