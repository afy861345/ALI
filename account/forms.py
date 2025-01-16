from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
class User_form(UserCreationForm):
    email=forms.CharField(max_length=150,required=True,widget=forms.EmailInput())
    class Meta:
        model=User
        fields=[
            'username','email','password1','password2'
        ]