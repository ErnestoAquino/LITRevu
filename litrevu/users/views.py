from django.shortcuts import render
from users import forms


def login_page(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            pass

    return render(request, 'users/login.html', {"form": form})

