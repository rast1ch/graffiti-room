from django.contrib.auth.models import AbstractUser
from django.db import models


class Crew(models.Model):
    """Модель для крю(групп райтеров)"""
    crew_name = models.CharField(('Название крю'),max_length=200)
    crew_slug = models.SlugField(max_length=200)

class Artist(AbstractUser):
    """Модель для райтеров"""
    username = models.CharField(max_length=200,unique=True)
    graffiti_name = models.CharField(('Ник райтера'),max_length=200)
    slug = models.SlugField(unique = True,default= str(username))
    email = models.EmailField(('E-mail'), max_length=254,unique=True)
    profile_image = models.ImageField(('Фото профиля'), blank=True)
    tag_image = models.ImageField(('Фото тэга'), blank=True)
    inst_url = models.URLField(('Instagram'))
    fb_url = models.URLField(('Facebook'))
    crew = models.ForeignKey(Crew, related_name='artists',null=True, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = ('Райтер')
        verbose_name_plural = ('Райтеры')

    


   

