from django import forms
from django.forms import modelformset_factory
from .models import (
    Post,
    Image
)


class PostModelForm(forms.ModelForm):
    description = forms.CharField(label="Описание",widget=forms.Textarea,)
    class Meta:
        model = Post
        exclude = ['author', 'slug', 'active', 'likes']


class PostUpdateForm(forms.ModelForm):
    description = forms.CharField(label="Описание",widget=forms.Textarea,)
    
    class Meta:
        model = Post
        fields = ('description',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Изображение')

    class Meta:
        model = Image
        fields = ('image',)


ImageFormSet = modelformset_factory(Image,
                                    form=ImageForm, extra=3)
