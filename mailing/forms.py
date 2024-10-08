from django.forms import ModelForm, BooleanField, DateTimeField

from mailing.models import Message, Mailing, Client


class StyleFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("autor",)


class MailingForm(StyleFormMixin,DateTimeField, ModelForm):
    class Meta:
        model = Mailing
        exclude = ("autor","is_active", "status")


class ModeratorMailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ("is_active",)


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ("autor",)
