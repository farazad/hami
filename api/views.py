from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Profile, FollowerCount, AlertSetting
from .serializers import ProfileSerializer, FollowerCountSerializer, AlertSettingSerializer
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='top-insights')
    def top_insights(self, request):
        now = timezone.now()
        since = now - timezone.timedelta(hours=24)
        results = []
        for profile in Profile.objects.all():
            counts = FollowerCount.objects.filter(profile=profile, timestamp__gte=since).order_by('timestamp')
            if counts.count() >= 2:
                change = counts.last().count - counts.first().count
                results.append({
                    'profile': profile.username,
                    'platform': profile.platform,
                    'change': change,
                })
        # Top increases
        top_increases = sorted(results, key=lambda x: x['change'], reverse=True)[:5]
        # Top decreases
        top_decreases = sorted(results, key=lambda x: x['change'])[:5]
        return Response({
            'top_increases': top_increases,
            'top_decreases': top_decreases,
        })

class FollowerCountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FollowerCount.objects.all()
    serializer_class = FollowerCountSerializer
    permission_classes = [permissions.IsAuthenticated]

class AlertSettingViewSet(viewsets.ModelViewSet):
    queryset = AlertSetting.objects.all()
    serializer_class = AlertSettingSerializer
    permission_classes = [permissions.IsAuthenticated]
