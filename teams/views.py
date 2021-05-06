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
from feed.models import SavedNewsItem

def index(request):
    if request.user.is_authenticated:
        followed_teams_api_ids = [team.api_id for team in request.user.profile.teams.all()]
        args = {
            'premier_league_teams': get_premier_league_teams(),
            'followed_teams_api_ids': followed_teams_api_ids,
        }
    return render(request, 'index.html', args)

def show(request, team_id):
    team_details = get_team_details(team_id)
    team_name = team_details['name']
    saved_news_item_titles = [item.title for item in request.user.profile.saved_news_items.all()]
    args = {
        'details': team_details,
        'results': get_team_results(team_id, 10),
        'headlines': get_team_news(team_name, 1, 20),
        'tweets': get_team_tweets(team_name, 10),
        'guardian_articles': get_guardian_articles(team_name, 1, 10),
        'user_profile_id': request.user.profile.id,
        'saved_news_item_titles': saved_news_item_titles,
        'team_id': team_id,
        'followed': followed
    }
    return render(request, 'show.html', args)

def follow_team(request, api_id, name):
    profile = request.user.profile
    try:
        team = Team.objects.get(api_id = api_id)
    except Team.DoesNotExist:
        team = Team(name = name, api_id = api_id)
        team.save()
    profile.follow_team(team)
    return redirect('/teams/')

def unfollow_team(request, api_id):
    profile = request.user.profile
    team = Team.objects.get(api_id = api_id)
    profile.unfollow_team(team)
    return redirect('/teams/')

def save_news_item(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id = request.POST.get("profile_id"))
        title = request.POST.get("title")
        url = request.POST.get("url")
        source = request.POST.get("source")
        date = request.POST.get("date")
        item = SavedNewsItem(profile = profile,
                             title = title,
                             url = url,
                             source = source,
                             date = date)
        item.save()
        profile.save_news_item(item)
        team_id = request.POST.get("team_id")
        return redirect("/teams/" + str(team_id))
    return redirect("/teams/")

def unsave_news_item(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id = request.POST.get("profile_id"))
        item = SavedNewsItem.objects.get(title = request.POST.get("title"))
        profile.unsave_news_item(item)
        team_id = request.POST.get("team_id")
        return redirect("/teams/" + str(team_id))
    return redirect("/teams/")
