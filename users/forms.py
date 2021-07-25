from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.core.exceptions import ValidationError
from .models import Artist


class ArtistLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label='Логин')
    password = forms.CharField(max_length=100, label='Пароль', widget=forms.PasswordInput)


class ArtistCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    slug = forms.CharField(max_length=200, widget=forms.HiddenInput, required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    class Meta:
        model = Artist
        fields = ('email', 'username', 'slug', 'password1', 'password2')


class ArtistChangeForm(UserChangeForm):
    password = forms.CharField(max_length=60, widget=forms.HiddenInput, required=False)

    class Meta:
        model = Artist
        fields = [
            'username', 'graffiti_name',
            'profile_image', 'tag_image',
            'inst_url', 'fb_url'
        ]
