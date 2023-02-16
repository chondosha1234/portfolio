from django import forms

class NameForm(forms.Form):

    textx = forms.CharField(
        label='Name for player X ',
        widget=forms.TextInput(
            attrs={
                'class': 'player',
                'placeholder': 'Enter name...',
                'size': '25'
            }
         )
    )

    texto = forms.CharField(
        label='Name for player O ',
        widget=forms.TextInput(
            attrs={
                'class': 'player',
                'placeholder': 'Enter name...',
                'size': '25'
            }
         )
    )
