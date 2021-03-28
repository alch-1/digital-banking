from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

APPETITE_CHOICES = [
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low'),
    ]

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))



class SignUpForm(forms.Form):
    name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    username = forms.CharField(max_length=30, required=False, help_text='Optional.')
    password1 = forms.CharField(max_length=30, required=False, help_text='Optional.')
    appetite= forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=APPETITE_CHOICES))


    # class Meta:
    #     model = User
    #     fields = ('name', 'username', 'password1', 'password2', )


