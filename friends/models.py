
from django.db import models

class UserProfile(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    interests = models.JSONField()
    
    class Meta:
      app_label = 'friends'
