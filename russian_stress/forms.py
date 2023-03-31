from django import forms

class TextForm(forms.Form):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Russian text here...',
            }
        ),
    )
