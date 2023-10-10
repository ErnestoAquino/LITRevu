"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from feed.views import FeedView

from feed.views import TicketCreateView
from feed.views import TicketUpdateView
from feed.views import TicketDeleteView

from feed.views import ReviewCreateView
from feed.views import ReviewUpdateView
from feed.views import ReviewDeleteView

from feed.views import PostView
import users.views
import feed.views
from litrevu import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", users.views.LoginPage.as_view(), name = "login"),
    path("signup/", users.views.signup_page, name = "signup"),
    path("logout/", users.views.LogoutUser.as_view(), name = "logout"),
    path("feed/", FeedView.as_view(), name = "feed"),
    path("posts/", PostView.as_view(), name = "posts"),
    path('follow/', users.views.FollowUserView.as_view(), name = 'follow_user'),
    path('unfollow/<int:pk>/', users.views.UnfollowUserView.as_view(), name = 'unfollow_user'),
    path('abonnements/', users.views.FollowedUsersView.as_view(), name = 'abonnements'),

    path("tickets/create/", TicketCreateView.as_view(), name = "ticket-create"),
    path("tickets/create/with-review/", feed.views.CreateTicketAndReviewView.as_view(), name = "ticket-review-create"),
    path("tickets/<int:pk>/update/", TicketUpdateView.as_view(), name = "ticket-update"),
    path("tickets/<int:pk>/delete/", TicketDeleteView.as_view(), name = "ticket-delete"),

    path("reviews/create/<int:ticket_id>/", ReviewCreateView.as_view(), name = "review-create"),
    path("reviews/<int:pk>/update/", ReviewUpdateView.as_view(), name = "review-update"),
    path("reviews/<int:pk>/delete/", ReviewDeleteView.as_view(), name = "review-delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
