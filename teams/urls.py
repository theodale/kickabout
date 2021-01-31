from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="teams"),
    path('<int:team_id>', views.show, name="team"),
]
