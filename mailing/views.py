from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from mailing.forms import MessageForm, MailingForm, ClientForm
from mailing.models import Mailing, Message, Client


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message



class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:mailing_create")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.autor = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")



class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingForm


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:index")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.autor = user
        mailing.status = "new"
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:index")


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:index")
    permission_required = "mailing.delete_mailing"


class ClientCreateView(LoginRequiredMixin, CreateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.autor = user
        mailing.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")


class ClientListView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client
