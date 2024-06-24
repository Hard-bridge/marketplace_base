from django import forms

class Reg(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    phone = forms.CharField()


class Auth(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
