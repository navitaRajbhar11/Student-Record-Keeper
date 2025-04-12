from django import forms

class UserForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    Profile_Images = forms.ImageField(required=False)  # Optional image field
