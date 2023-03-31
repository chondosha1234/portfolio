from django.shortcuts import render
from .utils import add_stress
from .forms import TextForm

def change_text(request):

    if request.method == "POST":
        form = TextForm(data=request.POST)
        if form.is_valid():
            text = add_stress(form.cleaned_data['text'])
    else:
        form = TextForm()
        text = ''

    context = {
        'text': text,
        'form': form,
    }
    return render(request, 'russian_stress.html', context)
