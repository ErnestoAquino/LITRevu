from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render
# from django.shortcuts import get_object_or_404
# from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from feed.forms import TicketForm
from feed.forms import ReviewForm
from feed.models import Ticket
from feed.models import Review


@method_decorator(login_required, name = "dispatch")
class HomePage(View):
    template_name = "feed/home.html"

    def get(self, request):
        user_tickets = Ticket.objects.filter(user = request.user).order_by('-time_create')
        return render(request, self.template_name, {"user_tickets": user_tickets})


@method_decorator(login_required, name = "dispatch")
class TicketCreatePage(FormView):
    template_name = "feed/ticket_create.html"
    form_class = TicketForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        ticket = form.save(commit = False)
        ticket.user = self.request.user
        ticket.save()
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "feed/ticket_update.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset = None):
        ticket = super().get_object(queryset)
        if ticket.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this ticket.")
        return ticket

    def form_valid(self, form):
        return super().form_valid(form)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "feed/ticket_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset = None):
        ticket = super().get_object(queryset)
        if ticket.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this ticket.")
        return ticket


@method_decorator(login_required, name='dispatch')
class CreateTicketAndReviewView(FormView):
    template_name = 'feed/ticket_and_review_create.html'
    form_class = TicketForm  # esto será accessible como 'form' en el template
    second_form_class = ReviewForm  # se tiene que manejar manualmente en la vista
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.POST or None)
        return context

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        ticket.save()

        form2 = self.second_form_class(self.request.POST)
        if form2.is_valid():
            review = form2.save(commit=False)
            review.ticket = ticket
            review.user = self.request.user
            review.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class PostView(View):
    template_name = "feed/posts.html"

    def get(self, request):
        user_tickets = Ticket.objects.filter(user=request.user).order_by('-time_create')
        user_reviews = Review.objects.filter(user=request.user).order_by('-time_create')
        return render(request, self.template_name, {"user_tickets": user_tickets, "user_reviews": user_reviews})


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "feed/review_update.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset=None):
        review = super().get_object(queryset)
        if review.ticket.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this review")
        return review

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        review = self.get_object()
        context['ticket'] = review.ticket
        return context
