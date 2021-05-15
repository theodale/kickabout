from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="teams"),
    path('<int:team_id>', views.show, name="team"),
    path('follow/<int:api_id>/<str:name>', views.follow_team, name='follow_team'),
    path('unfollow/<int:api_id>', views.unfollow_team, name='unfollow_team'),
]
