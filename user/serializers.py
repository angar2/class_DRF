from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from blog.serializers import ArticleSerializer

VALID_EMAIL_LIST = ["naver.com", "gmail.com", "yahoo.com"]

# class UserSignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = "__all__"

#     # super(): child class에서 parent class를 상속받는 후, child class에서 동일한 method를 사용할 경우, parent class의 method가 overriding(덮어쓰기)됨. => super()를 통해 parent class의 method 내용을 모두 가져다 사용함
#     def create(self, *args, **kwargs):
#         user = super().create(*args, **kwargs)
#         p = user.password
#         user.set_password(p) # hashing
#         user.save()
#         return user

#     def update(self, *args, **kwargs):
#         user = super().update(*args, **kwargs)
#         p = user.password
#         user.set_password(p) # hashing
#         user.save()
#         return user


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

    hobby = HobbySerializer(many=True, read_only=True) # input data가 queryset일 경우 many=True로 설정
    get_hobbys = serializers.ListField(required=False)

    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby", "get_hobbys"]


class UserSerializer(serializers.ModelSerializer):

    # 다른 serializer class를 가져다 사용할 수 있음
    # (sourec="userprofile")로 filed명도 변경 가능함
    userprofile = UserProfileSerializer()
    article = ArticleSerializer(many=True, source="article_set", read_only=True)

    # Custom validation: 기존 validation을 통과해야 사용됨
    def validate(self, data):
        try:
            http_method = self.context["request"].method
        except:
            http_method = ""
        if http_method == "POST":
            if data.get("email", "").split("@")[-1] not in VALID_EMAIL_LIST:
                raise serializers.ValidationError(
                    detail={"error": "유효한 이메일 주소가 아닙니다."}
                )
        return data

    # 기존의 create 함수를 덮어쓰기 때문에 기존 validation을 통과하지 않음
    # 기존 create 함수에서 제공하지 않은 기능을 추가하기 위해선 create를 custom 해야함
    def create(self, validated_data):
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])
        password = validated_data.pop("password")

        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        user_profile = UserProfileModel.objects.create(user=user, **user_profile)
        user_profile.hobby.add(*get_hobbys) # manytomany의 경우 추가하기 위해선 add를 사용함
        user_profile.save()

        return user

    def update(self, instance, validated_data):
        # instance에는 입력된 object가 담긴다.
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys",[])

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            
            setattr(instance, key, value)
        instance.save()

        user_profile_object = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_object, key, value)

        user_profile_object.save()
        user_profile_object.hobby.set(get_hobbys)

        return instance

    class Meta:
        model = UserModel
        fields = ["username", "password", "email", "fullname", "join_date", "userprofile", "article"]

        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'password': {'write_only': True}, # default : False
            'email': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
        }