from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  # form provided for registration

# SIGN UP
from account.models import Profile


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=26, required=True)
    email = forms.EmailField(required=True)

    # we add the email field
    # we customize the form with new field (the fields need to be in the User model)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class ProfileViewForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('origin',)
