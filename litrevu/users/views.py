from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View
from users import forms


class LoginPage(View):
    form_class = forms.LoginForm
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name,
                      {"form": form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                message = f"Invalid credentials."
        return render(request, self.template_name,
                      {"form": form, 'message': message})


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect("login")


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            pass
    return render(request, 'users/signup.html', context = {'form': form})
