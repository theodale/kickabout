from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="teams"),
    path('<int:team_id>', views.show, name="team"),
    path('follow/<int:api_id>/<str:name>', views.follow_team, name='follow'),
    path('unfollow/<int:api_id>', views.unfollow_team, name='unfollow'),
    path('save-news-item', views.save_news_item, name="team_save_news_item"),
    path('unsave-news-item', views.unsave_news_item, name="team_unsave_news_item")
]
