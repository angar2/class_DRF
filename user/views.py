from unittest import result
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from user.serializers import UserSerializer

from main.permissions import RegisterMoreThanAWeek

# FBV: Function Base View
# CBV: Class Base View (함수명은 API method를 이용함 / 별도 지정 x)
class UserView(APIView):
    
    # 해당 class의 접근 권한 설정
    # permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [RegisterMoreThanAWeek]

    # 사용자 정보 조회
    def get(self, request):
        user = request.user

        # 디버깅 시 사용하면 좋은 구문
        #  dir: 'user'에서 사용할 수 있는 모든 것을 보여줌
        # print(dir(user)) 

        # 역참조를 사용했을 때
        # one-to-one field는 예외로 _set이 붙지 않음
        hobbys = user.userprofile.hobby.all() # user Model에는 userprofile field가 없지만 UserProfile에서 user를 외래키를 사용하기 때문에 가능함

        # 역참조를 사용하지 않았을 때
        # user_profile = UserProfile.objects.get(user=user)
        # hobbys = user_profile.hobby.all()

        # for hobby in hobbys:
        #     # exculde : 매칭 된 쿼리만 제외, filter와 반대
        #     # annotate : 필드 이름을 변경해주기 위해 사용, 이외에도 원하는 필드를 추가하는 등 다양하게 활용 가능
        #     # values / values_list : 지정한 필드만 리턴 할 수 있음. values는 dict로 return, values_list는 tuple로 ruturn
        #     # F() : 객체에 해당되는 쿼리를 생성함
        #     hobby_members = hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username', flat=True)
        #     hobby_members = list(hobby_members)
        #     print(f"hobby : {hobby.name} / hobby members : {hobby_members}")

        return Response(UserSerializer(request.user).data)

    # 회원가입
    def post(self, request):

        return Response({"message": "post method!"})

    # 회원 정보 수정
    def put(self, request):

        return Response({"message": "put method!"})

    # 회원 탈퇴
    def delete(self, request):

        return Response({"message": "delete method!"})


class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    # 로그인
    @csrf_exempt # 한번하고 지우기
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        # 회원 정보 인증
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)

    def delete(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공!"}, status=status.HTTP_200_OK)