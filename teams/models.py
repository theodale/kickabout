from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=200)
    api_id = models.IntegerField()

    def __str__(self):
        return str(self.team_name)
