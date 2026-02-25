from django.shortcuts import render
from ..models.forms import TarefaForm

def home(request):
    contexto = {
        'nome': 'Pedro'
    }
    return render(request, 'home.html', contexto)


def adicionar_tarefa(request):
    contexto = {
        "form": TarefaForm()
    }
    return render(request, 'add.html', contexto)
