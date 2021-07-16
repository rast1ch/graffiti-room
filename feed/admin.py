from django.contrib import admin
from .models import Post,Image


class ImageInline(admin.StackedInline):
    model = Image

class PostAdminModel(admin.ModelAdmin):
    fields = ['user','slug','description','likes','active']
    ordering = ('uploaded',)
    inlines = [ImageInline]
    list_display= ['user', 'slug', 'description', 'active']

admin.site.register(Post,PostAdminModel)
admin.site.register(Image)