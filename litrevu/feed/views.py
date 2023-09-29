from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormView
from feed.forms import TicketForm


@method_decorator(login_required, name = "dispatch")
class HomePage(View):
    template_name = "feed/home.html"

    def get(self, request):
        return render(request, self.template_name)


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
