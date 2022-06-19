from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(("카테고리 이름"), max_length=50, unique=True)
    description = models.CharField(("카테고리 설명"), max_length=200)

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField(("글 제목"), max_length=200)
    body = models.TextField(("글 내용"), max_length=1000)
    category = models.ManyToManyField('Category')

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey('Article', verbose_name="게시글", on_delete=models.CASCADE)
    author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    content = models.CharField(("댓글"), max_length=200)

    def __str__(self):
        return self.author