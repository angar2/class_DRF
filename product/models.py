from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField(("글 제목"), max_length=200)
    thumbnail = models.FileField(("썸네일"), upload_to='img/')
    description = models.TextField(("글 내용"), max_length=1000)
    post_date = models.DateField('등록일', auto_now_add=True)
    start_date = models.DateField('노출 시작일', default=timezone.now)
    end_date = models.DateField('노출 종료일', default=timezone.now)

