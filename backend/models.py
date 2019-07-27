from django.db import models
import uuid
from mdeditor.fields import MDTextField
from django.urls import reverse


# Create your models here.

class Author(models.Model):
    nickname = models.CharField(max_length=30, blank=False, default='Anonymous', verbose_name=u'作者')
    avatar = models.ImageField(upload_to='./uploads/avatars/', verbose_name=u'头像')
    comments = models.CharField(max_length=200, blank=True, verbose_name=u'评论')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name_plural = u'作者'
        verbose_name = u'作者'


class Image(models.Model):
    image = models.ImageField(upload_to='./uploads/images/%Y', verbose_name=u'插图')

    def __str__(self):
        return self.image.path

    class Meta:
        verbose_name_plural = u'图片'
        verbose_name = u'图片'


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, blank=False, default='uncategoried', verbose_name=u'标签')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'


class Article(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    title = models.CharField(max_length=100, blank=False, default='No title', verbose_name=u'标题')
    content = MDTextField(verbose_name=u'正文')
    # author = models.CharField(max_length=30, blank=False, default='Anonymous')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=u'作者')
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, default=None, null=True, blank=True, verbose_name=u'标签')
    # content = models.TextField()
    file = models.FileField(upload_to='./uploads/markdown/%Y', verbose_name=u'文件路径')
    views = models.PositiveIntegerField(default=0, verbose_name=u'阅读数')

    is_top = models.BooleanField(default=False, verbose_name=u'顶置文章')
    is_show = models.BooleanField(default=True, verbose_name=u'发布状态')

    post_type = models.CharField(max_length=20,
                                 choices=(('post', u'博客文章'),
                                          ('about', u'关于页面'),
                                          ('project', u'我的项目')),
                                 default='post',
                                 verbose_name=u'类型')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-is_top', '-created_time']
        verbose_name_plural = u'博客文章'
        verbose_name = u'博客文章'
