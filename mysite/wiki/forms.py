from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    """
    The UserLoginForm is a simple implementation of AuthenticationForm
    used to provide a username, password and any error messages to
    the login.html template.
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    error = None
