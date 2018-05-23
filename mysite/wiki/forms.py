from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm

from wiki.models import UploadedFile


class UserLoginForm(AuthenticationForm):
    """
    The UserLoginForm is a simple implementation of AuthenticationForm
    used to provide a username, password and any error messages to
    the login.html template.
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    error = None


class FileUploadForm(ModelForm):
    class Meta:
        model = UploadedFile
        fields = '__all__'
