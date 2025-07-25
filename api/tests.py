import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Profile, AlertSetting, FollowerCount
from .tasks import check_follower_counts
from unittest.mock import patch
import base64

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def api_client(user):
    client = APIClient()
    credentials = base64.b64encode(b'testuser:testpass').decode('utf-8')
    client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
    return client

@pytest.mark.django_db
def test_profile_crud(api_client):
    # Create
    url = reverse('profile-list')
    data = {'username': 'john', 'platform': 'twitter', 'telegram_chat_id': '12345'}
    resp = api_client.post(url, data)
    assert resp.status_code == 201
    # Retrieve
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data[0]['username'] == 'john'
    # Update
    profile_id = resp.data[0]['id']
    url_detail = reverse('profile-detail', args=[profile_id])
    resp = api_client.patch(url_detail, {'platform': 'instagram'})
    assert resp.status_code == 200
    assert resp.data['platform'] == 'instagram'

@pytest.mark.django_db
def test_alert_setting_crud(api_client):
    # Need a profile first
    profile = Profile.objects.create(username='jane', platform='twitter', telegram_chat_id='54321')
    url = reverse('alertsetting-list')
    data = {'profile': profile.id, 'milestone': 1000}
    resp = api_client.post(url, data)
    assert resp.status_code == 201
    # Retrieve
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data[0]['milestone'] == 1000

@pytest.mark.django_db
def test_follower_count_retrieve(api_client):
    profile = Profile.objects.create(username='bob', platform='twitter', telegram_chat_id='11111')
    FollowerCount.objects.create(profile=profile, count=950)
    url = reverse('followercount-list')
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data[0]['count'] == 950

@pytest.mark.django_db
def test_authentication_required():
    client = APIClient()
    url = reverse('profile-list')
    resp = client.get(url)
    assert resp.status_code == 403 or resp.status_code == 401

@pytest.mark.django_db
def test_celery_task_milestone(monkeypatch):
    profile = Profile.objects.create(username='alice', platform='twitter', telegram_chat_id='99999')
    alert = AlertSetting.objects.create(profile=profile, milestone=1000, notified=False)
    FollowerCount.objects.create(profile=profile, count=999)
    monkeypatch.setattr('random.randint', lambda a, b: 2)
    with patch('api.tasks.send_telegram_message') as mock_send:
        check_follower_counts()
        alert.refresh_from_db()
        assert mock_send.called
        assert alert.notified is True
