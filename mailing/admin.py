from django.contrib import admin
from mailing.models import Client, Message, Mailing, Attempt
from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "token")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("status", "message")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("status", "created_at", "mailing")
