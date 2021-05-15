from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teams = models.ManyToManyField('teams.Team')
    saved_news_items = models.ManyToManyField('feed.SavedNewsItem')

    def follow_team(self, team):
        self.teams.add(team)

    def unfollow_team(self, team):
        self.teams.remove(team)

    def save_news_item(self, news_item):
        self.saved_news_items.add(news_item)

    def unsave_news_item(self, news_item):
        self.saved_news_items.remove(news_item)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)