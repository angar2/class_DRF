from django.db import models

# Create your models here.
class Category(models.Model):
    category = models.CharField(("카테고리 이름"), max_length=50, unique=True)
    description = models.CharField(("카테고리 설명"), max_length=200)


class Article(models.Model):
    author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField(("글 제목"), max_length=200)
    body = models.TextField(("글 내용"), max_length=1000)
    category = models.ManyToManyField('Category')