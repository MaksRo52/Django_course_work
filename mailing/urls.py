from django.urls import path
from django.views.decorators.cache import cache_page
from mailing.apps import MailingConfig
from mailing.views import (
    MailingCreateView,
    MailingDetailView,
    MailingDeleteView,
    MailingUpdateView,
    MailingListView,
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClientDeleteView,
    MessageCreateView,
    MessageListView,
    MessageDetailView,
    MessageUpdateView,
    MessageDeleteView,
    IndexView, AttemptListView,
)

app_name = MailingConfig.name

urlpatterns = [
    path("", cache_page(60)(IndexView.as_view()), name="index"),
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("update/<int:pk>", MailingUpdateView.as_view(), name="mailing_update"),
    path("delete/<int:pk>", MailingDeleteView.as_view(), name="mailing_delete"),
    path(
        "mailing/<int:pk>",
        cache_page(60)(MailingDetailView.as_view()),
        name="mailing_detail",
    ),
    path("client_create/", ClientCreateView.as_view(), name="client_create"),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path(
        "client_detail/<int:pk>/",
        cache_page(60)(ClientDetailView.as_view()),
        name="client_detail",
    ),
    path("client_update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client_delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path(
        "message_detail/<int:pk>/",
        cache_page(60)(MessageDetailView.as_view()),
        name="message_detail",
    ),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("client_create/", ClientCreateView.as_view(), name="client_create"),
    path("clients/", ClientListView.as_view(), name="client_list"),
    path(
        "client_detail/<int:pk>",
        cache_page(60)(ClientDetailView.as_view()),
        name="client_detail",
    ),
    path("client_update/<int:pk>", ClientUpdateView.as_view(), name="client_update"),
    path("client_delete/<int:pk>", ClientDeleteView.as_view(), name="client_delete"),
    path("attempts/", AttemptListView.as_view(), name="attempt_list")
]
