from django.db import models
from users.models import Artist


class Post(models.Model):
    """Класс постов для ленты"""
    author = models.ForeignKey(Artist, related_name='posts', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=6, unique=True, null=True)
    description = models.TextField()
    likes = models.PositiveIntegerField(default=1)
    uploaded = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)


class Image(models.Model):
    """Класс картинок для постов(т.к можно положить много картинок в пост)"""
    post = models.ForeignKey(Post, blank=True, related_name='images', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/')
