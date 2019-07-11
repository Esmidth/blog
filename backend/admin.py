from django.contrib import admin

# Register your models here.

from .models import Author, Image, Article, Tag

admin.site.register(Author)
admin.site.register(Image)
admin.site.register(Article)
admin.site.register(Tag)
