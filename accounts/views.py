# accounts

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import UserCustomChangeForm, ProfileForm, CustomUserCreationForm
from .models import Profile

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:list')
        
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form':form
    }

    return render(request, 'accounts/signup.html', context)
    

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            
            return redirect(request.GET.get('next') or 'posts:list')
        
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/login.html', context)
    

def logout(request):
    auth_logout(request)
    return redirect('posts:list')

def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = {'people':people,}
    return render(request, 'accounts/people.html', context)
    
    
@login_required
def update(request):
    if request.method == 'POST':
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('people', request.user.username)
    else:
        form = UserCustomChangeForm(instance=request.user)
    
    context = {'form':form}
    return render(request, 'accounts/update.html', context)

@login_required
def delete(request):
    if request.method == "POST":
        request.user.delete()
    return redirect('posts:list')
    
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('posts:list')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'accounts/change_password.html', context)
    
@login_required
def profile_update(request):
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method=="POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('people', request.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    context = {'profile_form':profile_form}
    return render(request, 'accounts/profile.html', context)
    
@login_required
def follow(request, user_pk):
    people = get_object_or_404(get_user_model(), pk=user_pk)
    # people이 팔로워하고 있는 모든 유저에 현재 접속 유저가 있다면,
    # 언팔로우
    if request.user in people.followers.all():
        people.followers.remove(request.user)
        
    # 아니면 팔로우
    else:
        people.followers.add(request.user)
    return redirect('people', people.username)