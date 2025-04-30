from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_events")
    
    def __str__(self):
        return self.title
    
    def participant_count(self):
        return self.participations.filter(is_attending=True).count()
    
    class Meta:
        ordering = ['date']

class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participations")
    is_attending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'event']
        
    def __str__(self):
        status = "participera" if self.is_attending else "ne participera pas"
        return f"{self.user.username} {status} à {self.event.title}"