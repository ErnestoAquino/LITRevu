from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from feed.forms import TicketForm


@login_required
def home(request):
    return render(request, "feed/home.html")


@method_decorator(login_required, name = "dispatch")
class HomePage(View):
    template_name = "feed/home.html"

    def get(self, request):
        return render(request, self.template_name)


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit = False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')

    form = TicketForm()
    return render(request, 'feed/ticket_create.html', {'form': form})
