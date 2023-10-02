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
from feed.models import Ticket


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
    success_url = reverse_lazy("home")

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
