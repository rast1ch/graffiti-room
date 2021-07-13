from django.db import models
import random
import string
from users.models import Artist


def rand_slug():
    """Формирования случайного url"""
    return ''.join(random.choice(string.ascii_letters + string.digits)for _ in range(6))

class Post(models.Model):
    """Класс постов для ленты"""
    user = models.ForeignKey(Artist, related_name='posts',on_delete=models.CASCADE)
    slug = models.SlugField(max_length=6,unique=True,default=rand_slug())
    description = models.TextField()
    likes = models.PositiveIntegerField()
    uploaded = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    """Класс картинок для постов(т.к можно положить много картинок в пост)"""
    post = models.ForeignKey(Post,related_name='images',on_delete=models.CASCADE)
    img = models.ImageField()
