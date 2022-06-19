from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

class HobbySerializer(serializers.ModelSerializer):

    # SerializerMethodField을 사용하기 위해선 변수 지정 후 "get_" 함수를 만들어야함
    same_hobby_users = serializers.SerializerMethodField()
    def get_same_hobby_users(self, obj):
        # obj: hobby model의 object
        
        # 기존 for문 활용 방식
        # user_list = []
        # for user_profile in obj.userprofile_set.all():
        #     user_list.append(user_profile.user.username)
        # return user_list

        # list 축약 방식
        return [user_profile.user.username for user_profile in obj.userprofile_set.all()]

    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]
        # fields = ["name", "userprofile_set"] # 별도의 field 지정 없이도 역참조로 사용 가능함


class UserProfileSerializer(serializers.ModelSerializer):

    hobby = HobbySerializer(many=True) # input data가 queryset일 경우 many=True로 설정

    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby"]


class UserSerializer(serializers.ModelSerializer):

    # 다른 serializer class를 가져다 사용할 수 있음
    # (sourec="userprofile")로 filed명도 변경 가능함
    userprofile = UserProfileSerializer()

    class Meta:
        model = UserModel
        fields = ["username", "email", "fullname", "join_date", "userprofile"]