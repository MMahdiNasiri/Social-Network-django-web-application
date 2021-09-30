from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UpdateImage(forms.ModelForm):
    profileImage = forms.FileField(required=False)

    class Meta:
        model = Profile
        fields = ['profileImage']


class UpdateProfile(forms.ModelForm):
    location = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control col-6'}),
        label='موقعیت', required=False)
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={'style': 'height: 100px', 'class': 'form-control col-6'}),
        label='بیو', required=False)

    class Meta:
        model = Profile
        fields = ['location', 'bio']


class UpdateUser(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control col-6'}),
        label='نام', required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control col-6'}),
        label='نام خانوادگی', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
