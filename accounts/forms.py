from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(forms.ModelForm):

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"}),
        validators=[validate_password],
    )

    confirm_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password"}),
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["username"]
        widgets = {forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username",
          })
        }
        error_messages = {
            "text": {"required": "Must enter a username"}
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
