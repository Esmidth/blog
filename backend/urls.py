from django.urls import path
from . import views as BlogViews

app_name = 'backend'

urlpatterns = [
    path('', BlogViews.Index().index, name='Index'),
    path('tags/', BlogViews.Tag, name='Tags'),
    path('archives/', BlogViews.Archives, name='Archives'),
    path('about/', BlogViews.About, name='About'),
    path('project/', BlogViews.Project, name='Project'),
    path('tag/<tag>/', BlogViews.Index().tags, name='tag'),
    path('article/<int:pk>/', BlogViews.Detail.as_view(), name='articles'),
    # path('content.json/',BlogViews.search
]
