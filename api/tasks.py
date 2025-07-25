from celery import shared_task
from .models import Profile, FollowerCount, AlertSetting
import random
import requests
from django.utils import timezone

def send_telegram_message(chat_id, text):
    token = 'YOUR_BOT_TOKEN'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        pass

@shared_task
def check_follower_counts():
    for profile in Profile.objects.all():
        last_count = FollowerCount.objects.filter(profile=profile).order_by('-timestamp').first()
        new_count = (last_count.count if last_count else 900) + random.randint(-10, 30) #mocking follower count changes
        FollowerCount.objects.create(profile=profile, count=new_count, timestamp=timezone.now())
        try:
            alert = AlertSetting.objects.get(profile=profile)
            if not alert.notified and new_count >= alert.milestone:
                send_telegram_message(profile.telegram_chat_id, f"{profile.username} reached {alert.milestone} followers!")
                alert.notified = True
                alert.save()
        except AlertSetting.DoesNotExist:
            pass 