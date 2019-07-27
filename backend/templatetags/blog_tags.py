from backend.models import Article, Tag, Author, Image
from django import template
from django.db.models.aggregates import Count
from blog.settings import SITE_CONFIGS

register = template.Library()


@register.simple_tag
def get_recent_comments(num=5):
    pass


@register.simple_tag
def get_recent_posts(num=5):
    return Article.objects.filter(is_show=True).order_by('-created_time')[:num]


@register.simple_tag
def get_archives():
    return Article.objects.filter(is_show=True).dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_tags():
    tags_style = [
        "font-size:19px;color:#777",
        "font-size:14px;color:#999",
        "font-size:16.5px;color:#888",
        "font-size:24px;color:#555",
        "font-size:21.5px;color:#666"
    ]
    tags = Tag.objects.filter(article__is_show=True).annotate(num_posts=Count('article')).filter(
        num_posts__gt=0).order_by(
        '-num_posts')[:20]
    return {'tag_style': tags_style, 'tags': tags}


@register.simple_tag
def get_links():
    pass


@register.simple_tag
def get_site_configs():
    return SITE_CONFIGS
