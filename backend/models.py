from django.db import models
import uuid


# Create your models here.

class Author(models.Model):
    nickname = models.CharField(max_length=30, blank=False, default='Anonymous')
    avatar = models.ImageField(upload_to='./uploads/avatars/')
    comments = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nickname


class Image(models.Model):
    image = models.ImageField(upload_to='./uploads/images/%Y')

    def __str__(self):
        return self.image.path


class Tag(models.Model):
    tag = models.CharField(max_length=50, blank=False, default='uncategorized')

    def __str__(self):
        return self.tag


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, default='No title')
    # author = models.CharField(max_length=30, blank=False, default='Anonymous')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='./uploads/markdown/%Y')

    def __str__(self):
        return self.title
