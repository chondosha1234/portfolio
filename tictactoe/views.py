from django.shortcuts import render

# Create your views here.
def main_page(request):
    if 'textx' in request.POST:
        playerx = request.POST['textx']
    else:
        playerx = "X"

    if 'texto' in request.POST:
        playero = request.POST['texto']
    else:
        playero = "O"

    context = {
        'playerx': playerx,
        'playero': playero,
    }
    return render(request, 'tictactoe.html', context)

def start_page(request):
    return render(request, 'tictactoe_start.html')
