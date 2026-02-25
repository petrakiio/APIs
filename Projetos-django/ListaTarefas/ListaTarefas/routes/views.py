from django.shortcuts import render


def home(request):
    contexto = {
        'nome':'Pedro'
    }
    return render(request,'templates/index.html',contexto)

