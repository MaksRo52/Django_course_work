import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from blog.models import Blog
from mailing.forms import MessageForm, MailingForm, ClientForm, ModeratorMailingForm
from mailing.models import Mailing, Message, Client, Attempt


class IndexView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["count_mailing"] = len(Mailing.objects.all())
        context_data["count_active_mailing"] = len(
            Mailing.objects.filter(is_active=True)
        )
        context_data["clients"] = len(Client.objects.all())
        context_data["blog_list"] = random.sample(
            list(Blog.objects.all()), len(list(Blog.objects.all()))
        )[:3]
        return context_data


class MessageListView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    login_url = "users:login"
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    login_url = "users:login"
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.autor = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "users:login"
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_form_class(self):
        user = self.request.user
        if user != self.object.autor:
            raise PermissionDenied
        else:
            return self.form_class


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "users:login"
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def get_form_class(self):
        user = self.request.user
        if user != self.object.autor:
            raise PermissionDenied
        else:
            return self.form_class


class MailingListView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
    login_url = "users:login"
    model = Mailing
    form_class = MailingForm


class MailingCreateView(LoginRequiredMixin, CreateView):
    login_url = "users:login"
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

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

    def get_form_class(self):
        user = self.request.user
        if user == self.object.autor:
            return MailingForm
        elif user.has_perm("mailing.can_disable_mailing"):
            return ModeratorMailingForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "users:login"
    model = Mailing
    success_url = reverse_lazy("mailing:index")

    def get_form_class(self):
        user = self.request.user
        if user != self.object.autor:
            raise PermissionDenied
        else:
            return self.form_class


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
    def get_form_class(self):
        user = self.request.user
        if user != self.object.autor:
            raise PermissionDenied
        else:
            return self.form_class


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "users:login"
    model = Client
    success_url = reverse_lazy("mailing:client_list")
    def get_form_class(self):
        user = self.request.user
        if user != self.object.autor:
            raise PermissionDenied
        else:
            return self.form_class


class ClientListView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client
    def get_form_class(self):
        user = self.request.user
        if user != self.object.autor:
            raise PermissionDenied
        else:
            return self.form_class


class AttemptListView(ListView):
    model = Attempt