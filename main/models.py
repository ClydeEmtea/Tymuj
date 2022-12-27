from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created']

class Event(models.Model):
    motherteam = models.ForeignKey('Team', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    place = models.TextField(null=True, blank=True)
    when = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['when']
