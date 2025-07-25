from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, FollowerCountViewSet, AlertSettingViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'follower-counts', FollowerCountViewSet)
router.register(r'alerts', AlertSettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 