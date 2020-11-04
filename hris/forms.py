from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255, label="User id")
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
