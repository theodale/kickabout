from django.shortcuts import render, redirect
from utils.kickabout_api_manager import get_feed
from django.contrib.auth.models import User
from .models import SavedNewsItem
from users.models import Profile

def feed(request, page_id):
    if request.user.is_authenticated:
        user_teams = request.user.profile.teams.all()
        feed = get_feed(user_teams, page_number = page_id)
        saved_news_items_titles = [item.title for item in request.user.profile.saved_news_items.all()]
        args = {
            'feed': feed,
            'page_id': page_id,
            'next_page_id': page_id + 1,
            'user_profile_id': request.user.profile.id,
            'saved_news_item_titles': saved_news_items_titles
        }
        return render(request, 'feed.html', args)
    else:
        return redirect("/teams/")
