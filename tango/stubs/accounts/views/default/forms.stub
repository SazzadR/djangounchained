from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'username'
        }
    ))
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'first_name'
            }
        )
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'last_name'
            }
        )
    )
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'email'
        }
    ))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password1'
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password2'
            }
        )
    )

    field_order = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2'
    ]

    class Meta:
        model = get_user_model()
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'username'
        }
    ))
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password'
            }
        )
    )

    field_order = [
        'username',
        'password',
    ]

    class Meta:
        model = get_user_model()
        fields = {
            'username',
            'password',
        }
