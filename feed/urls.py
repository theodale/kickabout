from django.urls import path
from . import views

urlpatterns = [
    path('<int:page_id>', views.feed, name="feed"),
    path('save-news-item', views.save_news_item, name="feed_save_news_item"),
    path('unsave-news-item', views.unsave_news_item, name="feed_unsave_news_item")
]
