from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

def home(request):
    return render(request, 'data.html')