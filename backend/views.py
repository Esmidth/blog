from django.shortcuts import render
from .models import Author, Article, Image, Tag
from .serializer import ArticleSerializer, AuthorSerializer, ImageSerializer, TagSerializer

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.utils.text import slugify
from django.http import FileResponse
from markdown.extensions.toc import TocExtension
import markdown
import json, re


class AuthorViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ImageViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class TagViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


def MD():
    return markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.admonition',
        TocExtension(slugify=slugify)
    ])


class Index:
    def __init__(self):
        self.per_page = 10

    def index(self, request):
        article_list = Article.objects.filter(is_show=True, post_type='post')
        page = request.GET.get('page')
        return self.get_data(article_list=article_list, page=page, request=request)

    def category(self, request, category):
        article_list = Article.objects.filter(category_name=category, is_show=True, post_type='post')
        page = request.GET.get('page')
        return self.get_data(article_list=article_list, page=page, request=request)

    def tags(self, request, tag):
        article_list = Article.objects.filter(tags__name=tag, is_show=True, post_type='post')
        page = request.GET.get('page')
        return self.get_data(article_list=article_list, page=page, request=request)

    def get_data(self, article_list, page, request):
        article_list = self.Pagination(article_list=article_list, page=page)
        for i in range(len(article_list)):
            md = MD()
            article_list[i].content = md.convert(article_list[i].content)
            article_list[i].toc = md.toc
        return render(request, '../templates/index.html', context={'article_list': article_list})

    def Pagination(self, article_list, page: int):
        paginator = Paginator(article_list, self.per_page)
        try:
            article_list = paginator.page(page)
        except PageNotAnInteger:
            article_list = paginator.page(1)
        except EmptyPage:
            article_list = paginator.page(paginator.num_pages)
        return article_list


class Detail(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if not article.is_show:
            return render(request, '../templates/error.html')

        md = MD()
        article.content = md.convert(article.content)
        article.toc = md.toc

        article.increase_views()
        return render(request, '../templates/article.html', context={'article': article})

    def post(self, request):
        pass


def Archives(request):
    years = Article.objects.filter(is_show=True, post_type='post').dates('created_time', 'year', order='DESC')
    article_list = Article.objects.filter(is_show=True, post_type='post').order_by('-created_time')
    return render(request, 'blog/archives.html', context={'years': years, 'article_list': article_list})


def About(request):
    article = Article.objects.filter(post_type='about').first()
    if article:
        md = MD()
        article.content = md.convert(article.content)
        article.doc = md.toc
        article.increase_views()
        return render(request, '../templates/article.html', context={'article': article})
    else:
        return render(request, '../templates/error.html')


def Project(request):
    article = Article.objects.filter(post_type='project').first()
    if article:
        md = MD()
        article.body = md.convert(article.body)
        article.toc = md.toc
        article.increase_views()
        return render(request, 'blog/project.html', context={'article': article})
    else:
        return render(request, 'error.html')


def download_img(request):
    file = open('./uploads/images/2019/adder.png', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="adder.png"'
    return response


class ImageTool:
    @staticmethod
    def get_new_random_file_name(file_name):
        find_type = False
        for c in file_name:
            if c == '.':
                find_type = True
        if find_type:
            type = file_name.split('.')[-1]
