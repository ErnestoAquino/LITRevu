from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic import FormView
from django.db import IntegrityError
from users import forms
from users.models import UserFollows, CustomUser


class LoginView(View):
    """
    View to manage the user login functionality.

    'LoginView' handles both GET and POST requests related to the login page.
    During a GET request, an empty login form is presented. During a POST
    request, the submitted credentials are authenticated. If they are valid,
    the user is logged in and redirected to the feed; otherwise, an error
    message is displayed.
    """
    form_class = forms.LoginForm
    template_name = 'users/login.html'

    def get(self, request):
        """
        Handle GET requests to the login page.

        Renders the login page with an unpopulated login form.
        """
        form = self.form_class()
        message = ''
        return render(request, self.template_name,
                      {"form": form, 'message': message})

    @method_decorator(require_POST)
    def post(self, request):
        """
        Handle POST requests to the login page.

        Authenticates the user's credentials. If they are valid, the user
        is logged in and redirected to the feed. If they are invalid, an
        error message is displayed.
        """
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("feed")
            else:
                message = "Invalid credentials."
        return render(request, self.template_name,
                      {"form": form, 'message': message})


class LogoutUserView(LogoutView):
    """
    View to handle user logout functionality with automatic redirection.

    `LogoutUserView` inherits from Django's `LogoutView` and is aimed to
    facilitate straightforward user logout actions, followed by a redirection
    to a specified page - in this case, the login page.
    """
    next_page = reverse_lazy('login')


class SignupView(FormView):
    """
    View to manage the user signup functionality.

    `SignupPageView` facilitates the creation of a new user account through
    a signup form. Upon receiving a GET request, it renders the signup page
    with the form. When handling a POST request, it attempts to create a new user
    and log them in. Upon successful account creation and login, the user is
    redirected to the URL specified as the successful login destination.
    """
    form_class = forms.SignupForm
    template_name = "users/signup.html"
    # success_url = settings.LOGIN_REDIRECT_URL
    success_url = reverse_lazy("feed")

    def form_valid(self, form):
        """
         Handle POST requests with valid form data.

        Creates a user, logs them in, and redirects to 'success_url'.
        """

        # Create a new user instance and save it to the database.
        user = form.save()

        # Log the user in.
        login(self.request, user)

        # Redirect to the URL specified as the login destination in settings.
        return super().form_valid(form)


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


class FollowUserView(LoginRequiredMixin, View):
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

    @method_decorator(require_POST)
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


class UnfollowUserView(LoginRequiredMixin, View):
    """
    View to handle the action of unfollowing a user.

    The view expects to receive a 'pk' (primary key) of the user to unfollow
    as part of the URL. This 'pk' is used to identify the followed user
    and delete the corresponding follow relationship.
    """

    @method_decorator(require_POST)
    def post(self, request, pk, *args, **kwargs):
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
