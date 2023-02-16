from django.shortcuts import render, redirect
from tictactoe.forms import NameForm

def main_page(request):
    form = NameForm(request.POST)

    if form.is_valid():
        playerx = request.POST['textx']
        playero = request.POST['texto']

        context = {
            'playerx': playerx,
            'playero': playero,
        }
        return render(request, 'tictactoe.html', context)
    
    return redirect('ttt:start_page')

def start_page(request):
    form = NameForm()
    context = {
        'form': form
    }
    return render(request, 'tictactoe_start.html', context)
