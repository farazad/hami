from rest_framework import serializers
from .models import Profile, FollowerCount, AlertSetting

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class FollowerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerCount
        fields = '__all__'

class AlertSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertSetting
        fields = '__all__' 