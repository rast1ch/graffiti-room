from django import forms
from django.forms import modelformset_factory
from .models import (
    Post,
    Image
)


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'slug', 'active', 'likes']


class PostUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea,label="Описание")
    
    class Meta:
        model = Post
        fields = ('description',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Image
        fields = ('image',)


ImageFormSet = modelformset_factory(Image,
                                    form=ImageForm, extra=3)
