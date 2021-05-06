from django.shortcuts import redirect, render
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

def unsave_news_item(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.POST.get("profile_id"))
        item = SavedNewsItem.objects.get(id=request.POST.get("item_id"))
        profile.unsave_news_item(item)
    return redirect("/accounts/profile/")
