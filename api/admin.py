from django.contrib import admin
from .models import Profile, FollowerCount, AlertSetting

admin.site.register(Profile)
admin.site.register(FollowerCount)
admin.site.register(AlertSetting)
