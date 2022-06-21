from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
# date filed:  2022-06-10
# DateField와 비교: user.join_date > datetim.now()
from django.utils import timezone
# datetime filed: 2022-06-10 10:40:20
# DateTimeField와 비교: user.join_date > timezone.now()
from rest_framework.exceptions import APIException
from rest_framework import status

# custom permission
class RegisterMoreThanAWeek(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # print(user.join_date)
        # print(datetime.now().date())
        # print(datetime.now().date() - timedelta(days=7))
        return bool(user.join_date < datetime.now().date() - timedelta(days=7))


class RegisterMoreThanThreeDays(BasePermission):
    
    message = '가입 후 3일 이상 지난 사용자만 사용하실 수 있습니다.'
        
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.join_date < (timezone.now() - timedelta(days=3)))


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrAWeekSignUp(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if bool(user.join_date < (timezone.now() - timedelta(days=7))) or user.is_admin:
            return True
            
        if user.is_authenticated and request.method in self.SAFE_METHODS: # GET
            return True
        
        return False