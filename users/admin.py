from django.contrib import admin
from .models import Artist

class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields =  prepopulated_fields = {"slug": ("username",)}

admin.site.register(Artist,ArtistAdmin)