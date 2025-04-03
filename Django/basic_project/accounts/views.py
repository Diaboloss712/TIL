from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.
def index(request):
    return redirect('accounts:index')

def signup(request):
    if request.user.is_authenticated():
        return redirect('accounts:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(user = request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)

def login(request):
    if request.user.is_authenticated():
        return redirect('accounts:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            auth_login(request, request.user)
            return redirect('accounts:index')
    else:
        form = AuthenticationForm(request)
    context = {
        'form': form,
    }
    return render(request, 'accounts/index.html', context)

@login_required()
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

@login_required()
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:update')
    else:
        form = CustomUserChangeForm(user = request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

@login_required()
def delete(request):
    pass