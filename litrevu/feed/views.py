from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.db.models import CharField
from django.db.models import Value
from itertools import chain
from feed.forms import TicketForm
from feed.forms import ReviewForm
from feed.models import Ticket
from feed.models import Review


class FeedView(LoginRequiredMixin, View):
    """
    View that aggregates and renders content for a user's feed.

    `FeedView` compiles and displays both `Review` and `Ticket` instances on a user’s feed.
    This involves retrieving the posts from users followed by the logged-in user. Both ticket
    and review instances are annotated with a content type to differentiate them in the template.
    They are then ordered by creation time and presented to the user.
    """
    def get_reviewed_ticket_ids(self, user):
        """
        Get the IDs of tickets reviewed by a particular user.

        Parameters:
        user: User object
            The user whose reviewed ticket IDs are being retrieved.

        Returns:
        QuerySet of Integers
            IDs of tickets that have been reviewed by the user.
        """
        return Review.objects.filter(user = user).values_list('ticket_id', flat = True)

    def get_users_viewable_reviews(self, user):
        """
        Gather reviews made by users that the specified user follows.

        Parameters:
        user: User object
            The user for whom viewable reviews are being retrieved.

        Returns:
        QuerySet of Review objects
            Reviews created by users that are followed by the specified user.
        """
        followed_users = user.following.values_list('followed_user', flat = True)
        return Review.objects.filter(user_id__in = followed_users)

    def get_users_viewable_tickets(self, user):
        """
        Gather tickets made by users that the specified user follows.

        Parameters:
        user: User object
            The user for whom viewable tickets are being retrieved.

        Returns:
        QuerySet of Ticket objects
            Tickets created by users that are followed by the specified user.
        """
        followed_users = user.following.values_list('followed_user', flat = True)
        return Ticket.objects.filter(user_id__in = followed_users)

    def get(self, request, *args, **kwargs):
        # Retrieve and annotate reviews and tickets visible to the user
        reviews = self.get_users_viewable_reviews(request.user)
        reviews = reviews.annotate(content_type = Value('REVIEW', CharField()))
        tickets = self.get_users_viewable_tickets(request.user)
        tickets = tickets.annotate(content_type = Value('TICKET', CharField()))

        # Get IDs of tickets reviewed by the user
        reviewed_ticket_ids = self.get_reviewed_ticket_ids(request.user)

        # Merge and sort the posts (reviews and tickets)
        posts = sorted(
            chain(reviews, tickets),
            key = lambda post: post.time_create,
            reverse = True
        )

        # Render the content on the user's feed
        return render(request,
                      'feed/feed.html',
                      context = {'posts': posts, 'reviewed_ticket_ids': reviewed_ticket_ids})


class TicketCreateView(LoginRequiredMixin, FormView):
    """
    View handling the creation of new Ticket instances.

    `TicketCreateView` simplifies the ticket creation process, presenting the user
    with a form (utilizing `TicketForm`) and managing the form validation and
    instance saving during POST requests. Upon successfully creating a new ticket,
    the user is navigated back to the "feed" page.
    """
    template_name = "feed/ticket_create.html"
    form_class = TicketForm
    success_url = reverse_lazy("feed")

    def form_valid(self, form):
        # Save form data into a ticket instance without committing to the database yet
        ticket = form.save(commit = False)

        # Associate the current user as the ticket's creator
        ticket.user = self.request.user

        # Finalize saving the ticket instance to the database
        ticket.save()

        # Redirect to the success URL
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for handling the update of a Ticket instance.

    The `TicketUpdateView` facilitates the process of updating a Ticket by displaying
    a form initialized with the existing Ticket data and handling the POST request
    upon form submission. Ensuring only the user who created the ticket can update it,
    and after successful update, the user is redirected to the "posts" page.
    """
    model = Ticket
    form_class = TicketForm
    template_name = "feed/ticket_update.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset = None):
        # Retrieve the ticket instance from the database
        ticket = super().get_object(queryset)

        # Check that the user requesting the update is the ticket creator
        if ticket.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this ticket.")
        return ticket

    def form_valid(self, form):
        # Save the form and redirect to the success URL
        return super().form_valid(form)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to manage the deletion of a Ticket instance.

    `TicketDeleteView` is designed to handle the deletion of a Ticket instance,
    ensuring that only the user who created the ticket can delete it. Upon
    successful deletion, users are redirected to the "posts" page.
    """
    model = Ticket
    template_name = "feed/ticket_delete.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset = None):
        # Retrieve the ticket instance
        ticket = super().get_object(queryset)

        # Validate that the user requesting the deletion is the ticket's creator
        if ticket.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this ticket.")
        return ticket


class CreateTicketAndReviewView(LoginRequiredMixin, FormView):
    """
    View to manage the creation of a Ticket and its associated Review.

    `CreateTicketAndReviewView` handles the presentation of the form for creating
    a new Ticket and its associated Review, ensuring only authenticated users
    can access it. It manages the rendering of two forms and ensures data
    consistency upon form submissions.
    """
    template_name = 'feed/ticket_and_review_create.html'
    form_class = TicketForm
    second_form_class = ReviewForm
    success_url = reverse_lazy('feed')

    def get_context_data(self, **kwargs):
        """
        Retrieve and extend the context data.

        Extends the default context data with the instance of `second_form_class`,
        initializing it with POST data if available.
        """
        context = super().get_context_data(**kwargs)

        # Add second form to the context if it's not already present
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.POST or None)
        return context

    def form_valid(self, form):
        # Create, but don't save the new ticket instance yet
        ticket = form.save(commit = False)

        # Assign the current user to the new ticket instance
        ticket.user = self.request.user

        # Save the ticket instance
        ticket.save()

        # Manually validate the second form
        form2 = self.second_form_class(self.request.POST)

        # Check the validity of the second form
        if form2.is_valid():

            # Create, but don't save the new review instance yet
            review = form2.save(commit = False)

            # Assign the current user and associated ticket to the new review instance
            review.ticket = ticket
            review.user = self.request.user

            # Save the review instance
            review.save()

            # Redirect to the success URL
            return super().form_valid(form)
        else:
            # If the second form is invalid, re-render the forms with the data
            return self.form_invalid(form)


class PostView(LoginRequiredMixin, View):
    """
    View to display user's tickets and reviews in the 'posts' page.

    `PostView` manages the rendering of the 'posts' page which displays the
    tickets and reviews created by the authenticated user. Both tickets and
    reviews are displayed in descending order based on their creation time.
    """
    template_name = "feed/posts.html"

    def get(self, request):
        # Retrieve tickets created by the user, ordered by creation time
        user_tickets = Ticket.objects.filter(user = request.user).order_by('-time_create')

        # Retrieve reviews created by the user, ordered by creation time
        user_reviews = Review.objects.filter(user = request.user).order_by('-time_create')

        # Render the page with the fetched tickets and reviews
        return render(request, self.template_name, {"user_tickets": user_tickets, "user_reviews": user_reviews})


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new review.

    `ReviewCreateView` is responsible for handling the creation of a new Review
    instance ensuring that only authenticated users can create a review and
    enforcing that a user cannot create a review for their own ticket. The view
    manages form rendering, context data preparation, and object creation upon
    valid form submission.
    """
    model = Review
    form_class = ReviewForm
    template_name = "feed/review_create.html"
    success_url = reverse_lazy("posts")

    def get_context_data(self, **kwargs):
        # Get default context data
        context = super().get_context_data(**kwargs)

        # Add related ticket to context data
        context['ticket'] = get_object_or_404(Ticket, pk = self.kwargs.get('ticket_id'))
        return context

    def form_valid(self, form):
        # Assign the requesting user and related ticket to the form instance
        form.instance.user = self.request.user
        form.instance.ticket = get_object_or_404(Ticket, pk = self.kwargs.get('ticket_id'))

        # Proceed to default form_valid behavior (save and redirect)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Retrieve related ticket
        ticket = get_object_or_404(Ticket, pk = kwargs.get('ticket_id'))

        # Check if user is trying to review their own ticket
        if ticket.user == request.user:
            raise PermissionDenied("You cannot review your own ticket")

        # Proceed to default dispatch behavior
        return super().dispatch(request, *args, **kwargs)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
     View to manage the update of a review.

    `ReviewUpdateView` manages the update process of a Review instance, ensuring
    only authenticated users can update a review and only their own reviews.
    It provides a form for editing and updates the instance upon valid submission.
    Additionally, it ensures the appropriate context is supplied to the template.
    """
    model = Review
    form_class = ReviewForm
    template_name = "feed/review_update.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset = None):
        # Retrieve the review instance
        review = super().get_object(queryset)
        # Validate that the user requesting the update is the review's creator
        if review.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this review")
        return review

    def form_valid(self, form):
        # Assign the requesting user to the form instance user
        form.instance.user = self.request.user
        # Proceed to default form_valid behavior (save and redirect)
        return super().form_valid(form)

    def get_context_data(self):
        # Get default context data
        context = super().get_context_data()

        # Add related ticket to context data
        review = self.get_object()
        context['ticket'] = review.ticket
        return context


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to manage the deletion of a review.

    'ReviewDeleteView' manages the deletion of an existing Review instance. It
    ensures that only authenticated users can delete a review and that users
    can only delete their own reviews. It manages template rendering and object
    deletion upon user confirmation.

    """
    model = Review
    template_name = "feed/review_delete.html"
    success_url = reverse_lazy("posts")

    # Retrieve the review instance
    def get_object(self, queryset = None):
        review = super().get_object(queryset)

        # Validate that the user requesting the deletion is the review's creator
        if review.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this review")
        return review
