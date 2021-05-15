from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from feed.models import SavedNewsItem

class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = '/teams/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("teams")

def home(request):
    if request.user.is_authenticated:
        return redirect("/teams/")
    else:
        return render(request, 'home.html')

def profile(request):
    if request.user.is_authenticated:
        args = {
            'user': request.user,
            'profile': Profile.objects.get(user=request.user)
        }
        return render(request, 'profile.html', args)
    else:
        return redirect("/teams/")

def save_news_item(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.POST.get("profile_id"))
        title = request.POST.get("title")
        url = request.POST.get("url")
        source = request.POST.get("source")
        date = request.POST.get("date")
        item = SavedNewsItem(profile=profile, title=title,
            url=url, source=source, date=date)
        item.save()
        profile.save_news_item(item)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unsave_news_item(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.POST.get("profile_id"))
        try:
            item = SavedNewsItem.objects.get(id=request.POST.get("item_id"))
        except SavedNewsItem.DoesNotExist:
            item = profile.saved_news_items.get(title = request.POST.get("title"))
        profile.unsave_news_item(item)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

