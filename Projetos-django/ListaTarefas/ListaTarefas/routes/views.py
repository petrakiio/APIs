from django.shortcuts import render


def home(request):
    contexto = {
        'nome': 'Pedro'
    }
    return render(request, 'home.html', contexto)


def adicionar_tarefa(request):
    return render(request, 'add.html')
