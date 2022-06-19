from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField('사용자 계정', max_length=50, unique =True)
    password = models.CharField('비밀번호', max_length=128)
    email = models.EmailField('이메일 주소', max_length=20)
    fullname = models.CharField('이름', max_length=20)
    join_date = models.DateField('가입일', auto_now_add=True)

    is_active = models.BooleanField(default=True) # 회원 활성화 여부
    is_admin = models.BooleanField(default=False) # 관리자 여부

    # 회원 ID로 어떤 field를 사용할 것인지 지정 (ex. 로그인)
    USERNAME_FIELD = 'username'
    # user 생성 시 필수로 입력 받을 field를 지정(지정하지 않더라도 선언은 되어있어야함)
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.username} / {self.email} / {self.fullname}"

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True
    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label): 
        return True
    
    # admin 권한 설정
    @property
    def is_staff(self): 
        return self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="유저", on_delete=models.CASCADE)
    introduction = models.TextField("자기소개")
    birthday = models.DateField("생일")
    age = models.IntegerField("나이")
    hobby = models.ManyToManyField("Hobby", verbose_name="취미")

    def __str__(self):
        return f"{self.user.username} 님의 프로필"

class Hobby(models.Model):
    name = models.CharField("취미", max_length=50)

    def __str__(self):
        return self.name