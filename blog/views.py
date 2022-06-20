from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from .models import Article, Category

from main.permissions import RegisterMoreThanThreeDays

# Create your views here.
class ArticleView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        titles = [article.title for article in articles]
        return Response({"게시물 정보": titles})

    permission_classes = [RegisterMoreThanThreeDays]
    def post(self, request):
        user = request.user
        title = request.data.get('title', '')
        categories = request.data.get('categories', [])
        content = request.data.get('content', '')

        if len(title) < 6:
            return Response({
                "error": "제목이 5글자 이하면 작성할 수 없습니다."
            })
        if len(content) < 21:
            return Response({
                "error": "내용이 20글자 이하면 작성할 수 없습니다."
            })
        if categories == '':
            return Response({
                "error": "카테고리가 비어 있습니다."
            })

        # categories = [Category.objects.get(name=categories)] # value를 'name'을 받을 때 사용
        new_article = Article(
            author = user,
            title = title,
            body = content
        )
        new_article.save()
        new_article.category.add(*categories)

        return Response({"message": "게시물이 저장되었습니다."}, status=status.HTTP_200_OK)

    def put(self, request):
        return Response({"message": "put method!"})
    def delete(self, request):
        return Response({"message": "delete method!"})
