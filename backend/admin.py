from django.contrib import admin

# Register your models here.

from .models import Author, Image, Article

admin.site.register(Author)
admin.site.register(Image)
admin.site.register(Article)
