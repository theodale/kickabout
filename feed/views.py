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

def save_news_item(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.POST.get("profile_id"))
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
        page_id = request.POST.get("page_id")
        return redirect("/feed/" + str(page_id))
    return redirect("/feed/1")

def unsave_news_item(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id = request.POST.get("profile_id"))
        item = SavedNewsItem.objects.get(title = request.POST.get("title"))
        profile.unsave_news_item(item)
        page_id = request.POST.get("page_id")
        return redirect("/feed/" + str(page_id))
    return redirect("/feed/1")
