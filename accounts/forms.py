from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name',)

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['username','password',]

class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name',]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'introduction',]
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # Meta class도 상속 받을 수 있다
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
        
        
