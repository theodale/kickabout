from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html', success_url="/accounts/profile/"), name="password_change"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', views.profile, name="profile"),
     path('save-news-item/', views.save_news_item, name="save_news_item"),
    path('unsave-news-item/', views.unsave_news_item, name="unsave_news_item")
]
