from django.shortcuts import render, redirect
from utils.kickabout_api_manager import get_feed
from django.contrib.auth.models import User

def feed(request):
    if request.user.is_authenticated:
        args = {
            'feed': get_feed(request.user.profile.teams.all(), 2)
        }
        return render(request, 'feed.html', args)
    else:
        return redirect("/teams/")
