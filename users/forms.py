from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import forms

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'bio')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'bio')


from django import forms
from .models import CustomUser

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # CustomUser modelini belgilang
        fields = ['first_name', 'last_name', 'email', 'bio', 'phone_number', 'avatar']
