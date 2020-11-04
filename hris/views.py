from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import LoginForm
from django.contrib import messages


# Create your views here.


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/org')
            else:
                return render(request, 'login.html', {'form': form, 'message': "Invalid Credentials!"})
        else:
            return render(request, 'login.html', {'form': form, 'message': "Invalid Credentials!"})
    return render(request, 'login.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
