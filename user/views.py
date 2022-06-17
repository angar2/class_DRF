from math import perm
from unittest import result
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt

# FBV: Function Base View
# CBV: Class Base View (함수명은 API method를 이용함 / 별도 지정 x)
class UserView(APIView):
    
    # 해당 class의 접근 권한 설정
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]

    # 사용자 정보 조회
    def get(self, request):
        return Response({"message": "get method!"})

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