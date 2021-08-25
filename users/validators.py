import re
from django import forms
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import ngettext
from difflib import SequenceMatcher
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    UserAttributeSimilarityValidator,
    NumericPasswordValidator,
    CommonPasswordValidator
)



#В валидаторах изменен только текст ошибок

class CustomCommonValidator(CommonPasswordValidator):

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise forms.ValidationError(
                ("Пароль слишком простой"),
                code='password_too_common',
            )

class CustomNumericValidator(NumericPasswordValidator):

    def validate(self, password, user=None):
        if password.isdigit():
            raise forms.ValidationError(
                ("Пароль не может состоять только из цифр"),
                code='password_entirely_numeric',
            )

class CustomSimilarityValidator(UserAttributeSimilarityValidator):

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise forms.ValidationError(
                        ("Пароль слишком похож на другие данные"),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )


class CustomLenghtValidator(MinimumLengthValidator):

     def validate(self, password, user=None):
            if len(password) < self.min_length:
                raise forms.ValidationError(
                    ngettext(
                        "Пароль должен состоять из как минимум %(min_length)d символов",
                        "Пароль должен состоять из как минимум %(min_length)d символа",
                        self.min_length
                    ),
                    code='password_too_short',
                    params={'min_length': self.min_length},)