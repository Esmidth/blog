from django.contrib import admin

# Register your models here.

from .models import Author, Image, Article, Tag


# admin.site.register(Author)
# admin.site.register(Image)
# admin.site.register(Article)
# admin.site.register(Tag)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['tag_name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'avatar', 'comments']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'author', 'tags', 'views', 'is_top',
                    'is_show', 'post_type']
