from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.forms.widgets import CheckboxInput, Select, DateTimeInput
from users.models import User


class StyleFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

            if isinstance(field.widget, DateTimeInput):
                field.widget.input_type = "datetime-local"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

class ManagerUserUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('is_active',)




