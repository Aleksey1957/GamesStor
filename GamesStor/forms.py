from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Придумайте имя пользователя',
            'class': 'form-input'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'example@email.com',
            'class': 'form-input'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Придумайте пароль',
            'class': 'form-input'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Повторите пароль',
            'class': 'form-input'
        })