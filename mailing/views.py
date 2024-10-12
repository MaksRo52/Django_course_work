import random
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
from blog.services import get_blog_from_cache
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
            list(get_blog_from_cache()), len(list(get_blog_from_cache()))
        )[:3]
        return context_data



class MessageListView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    model = Message


class MessageDetailView(LoginRequiredMixin,PermissionRequiredMixin, DetailView):
    login_url = "users:login"
    model = Message
    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user

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


class MessageUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    login_url = "users:login"
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user


class MessageDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    login_url = "users:login"
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user


class MailingListView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    model = Mailing


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = "users:login"
    model = Mailing
    form_class = MailingForm

    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user or user.has_perm("mailing.can_disable_mailing")


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


class MailingUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user or user.has_perm("mailing.can_disable_mailing")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.autor:
            return MailingForm
        elif user.has_perm("mailing.can_disable_mailing"):
            return ModeratorMailingForm
        raise PermissionDenied

    def form_valid(self, form):
        mailing = form.save()
        mailing.status = "new"
        mailing.save()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    login_url = "users:login"
    model = Mailing
    success_url = reverse_lazy("mailing:index")

    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user


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


class ClientUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = "users:login"
    model = Client
    success_url = reverse_lazy("mailing:client_list")

    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user


class ClientListView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client

    def has_permission(self):
        obj = self.get_object()
        user = self.request.user
        return obj.autor == user

class AttemptListView(ListView):
    model = Attempt