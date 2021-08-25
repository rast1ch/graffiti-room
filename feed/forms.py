from django import forms
from django.forms import modelformset_factory
from .models import (
    Post,
    Image
)


class PostModelForm(forms.ModelForm):
    """Форма для создания постов"""
    description = forms.CharField(label="Описание",widget=forms.Textarea,)
    class Meta:
        model = Post
        exclude = ['author', 'slug', 'active', 'likes']


class PostUpdateForm(forms.ModelForm):
    """Форма для изменения описания постов"""
    description = forms.CharField(label="Описание",widget=forms.Textarea,)
    
    class Meta:
        model = Post
        fields = ('description',)

class ImageForm(forms.ModelForm):
    """Форма из формсета для прикрепления изображений к постам"""
    image = forms.ImageField(label='Изображение')

    class Meta:
        model = Image
        fields = ('image',)


ImageFormSet = modelformset_factory(Image,
                                    form=ImageForm, extra=3)
