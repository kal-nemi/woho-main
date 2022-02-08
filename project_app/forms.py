# from django import forms
# from django.contrib.auth import get_user_model
# # from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
#
#
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     first_name = forms.CharField()
#     last_name = forms.CharField()
#
#     class Meta:
#         model = get_user_model
#         fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
#
#
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()
#     first_name = forms.CharField()
#     last_name = forms.CharField()
#
#     class Meta:
#         model = get_user_model
#         fields = ['email', 'first_name', 'last_name']


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = []
