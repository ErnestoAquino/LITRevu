from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import render
from users import forms


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                message = f"Hello, {user.username}! You are logged in."
            else:
                message = f"Invalid credentials."

    return render(request, 'users/login.html',
                  {"form": form, 'message': message})
