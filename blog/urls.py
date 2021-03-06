"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.conf import settings

from rest_framework import routers
from backend.views import AuthorViewSet, ArticleViewSet, ImageViewSet, TagViewSet

routers = routers.DefaultRouter()
routers.register(r'authors', AuthorViewSet)
routers.register(r'articles', ArticleViewSet)
routers.register(r'images', ImageViewSet)
routers.register(r'tags', TagViewSet)

urlpatterns = [
    path('api/', include(routers.urls)),
    # path('', TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),
    # path('hexo/', TemplateView.as_view(template_name="static_hexo.html")),
    # path('blog/', TemplateView.as_view(template_name='static_blog.html')),
    # path('vue/', TemplateView.as_view(template_name='hello_vue.html')),
    # path('index/', TemplateView.as_view(template_name='base.html')),
    # path('', TemplateView.as_view(template_name='simp/index.html'), name='home'),
    path('', include('backend.urls'), name='blog'),
    path(r'mdeditor/', include('mdeditor.urls')),
    # path('blog/', include('backend.urls'))
]

# if settings.DEBUG:
# static files (images,css,javascript,etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
