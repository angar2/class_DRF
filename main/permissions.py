from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
# date filed:  2022-06-10
# DateField와 비교: user.join_date > datetim.now()
from django.utils import timezone
# datetime filed: 2022-06-10 10:40:20
# DateTimeField와 비교: user.join_date > timezone.now()

# custom permission
class RegisterMoreThanAWeek(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        print(user.join_date)
        print(datetime.now().date())
        print(datetime.now().date() - timedelta(days=7))
        return bool(user.join_date < datetime.now().date() - timedelta(days=7))