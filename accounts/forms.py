from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email Address"
             }),
            'password': forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password"
             })
        }
        error_messages = {
            'email': {'required': "Must enter an email"},
            'password': {'required': "Must enter a password"}
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ""
        self.fields["password"].label = ""

class CreateAccountForm(forms.ModelForm):

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
        fields = ["email"]
        widgets = {"email": forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email Address"
        })}
        error_messages = {
            'email': {'required': "Must enter an email"}
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password didn't match!")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CreateAccountForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ""
