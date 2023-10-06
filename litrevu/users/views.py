from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db import IntegrityError
from users import forms
from users.models import UserFollows, CustomUser


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
                return redirect("feed")
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
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'users/signup.html', context = {'form': form})


class FollowedUsersView(LoginRequiredMixin, View):
    """
    FollowedUsersView is a class-based view that renders a list of users that the
    currently authenticated user is following.

    This view ensures that only authenticated users can access the page to see their
    followed users by using the LoginRequiredMixin.

    Methods
    -------
    get(self, request, *args, **kwargs):
        Handles GET requests. Retrieves and renders a list of followed users for the
        currently authenticated user.
    """
    def get(self, request, *args, **kwargs):
        followed_users = UserFollows.objects.filter(user=request.user)
        return render(request,
                      'users/followed_users.html',
                      {'followed_users': followed_users})


class FollowUserView(View):
    """
    View to handle user-following actions.

    This view is designed to handle POST requests that contain the username
    of the person to be followed. It has mechanisms to handle scenarios such as
    trying to follow oneself, trying to follow a user that doesn’t exist, and
    trying to follow a user that one is already following.

    Methods
    -------
    post(request, *args, **kwargs):
        Processes POST requests, attempting to create a following relationship
        and providing user feedback via messages.
    """
    def post(self, request, *args, **kwargs):
        # Retrieve the username to follow from the POST data.
        username_to_follow = request.POST.get('username_to_follow')

        # Check if the user is trying to follow themselves.
        if username_to_follow == request.user.username:
            messages.error(request, "You cannot follow yourself.")
            return redirect('abonnements')

        try:
            # Retrieve the user to follow from the database.
            user_to_follow = CustomUser.objects.get(username=username_to_follow)

            # Create a new follow relationship.
            UserFollows.objects.create(user=request.user, followed_user=user_to_follow)

            # Send a success message to the user.
            messages.success(request, f"You are now following {user_to_follow.username}!")
        except CustomUser.DoesNotExist:
            # Send an error message if the user to follow does not exist.
            messages.error(request, f"The user {username_to_follow} does not exist.")
        except IntegrityError:
            # Send an error message if the following relationship already exists.
            messages.error(request, f"You are already following {username_to_follow}!")
        # Redirect the user back to the 'abonnements' page.
        return redirect('abonnements')


class UnfollowUserView(View):
    """
    View to handle the action of unfollowing a user.

    The view expects to receive a 'pk' (primary key) of the user to unfollow
    as part of the URL. This 'pk' is used to identify the followed user
    and delete the corresponding follow relationship.
    """

    def get(self, request, pk, *args, **kwargs):
        follow = UserFollows.objects.filter(user=request.user, followed_user_id=pk).first()
        # Check if the following relationship is found.
        if follow:
            # Save the followed user's username for use in the message.
            followed_username = follow.followed_user.username

            # Delete the following relationship.
            follow.delete()

            # Send a success message to the user.
            messages.success(request, f"You have unfollowed {followed_username}.")
        else:
            # If the relationship is not found, send an error message to the user.
            messages.error(request, "User not found.")

        # Redirect the user back to the 'abonnements' page.
        return redirect('abonnements')
