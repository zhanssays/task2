from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
