from django.contrib import admin
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(UserProfileModel)