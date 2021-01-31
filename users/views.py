from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = '/teams/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("teams")
