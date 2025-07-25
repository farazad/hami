from django.db import models

# Create your models here.

class Profile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    platform = models.CharField(max_length=50)
    telegram_chat_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.platform}:{self.username}"

class FollowerCount(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class AlertSetting(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    milestone = models.IntegerField()
    notified = models.BooleanField(default=False)
