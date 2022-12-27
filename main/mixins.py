from .models import *

class TeamMixin(object):
    def get_queryset(self):
        return Team.objects.filter(user=self.request.user)

class EventMixin(object):
    def get_queryset(self):
        return Event.objects.filter(project__user=self.request.user)
