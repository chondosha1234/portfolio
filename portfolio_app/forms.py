from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(
         max_length=100,
         required=True,
         widget=forms.EmailInput(
             attrs={
                 "class": "form-control",
                 "placeholder": "Email Address"
             },
         ),
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Send a message..."
            }
        ),
        required=True
    )
