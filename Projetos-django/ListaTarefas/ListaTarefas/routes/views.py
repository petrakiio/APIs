from django.shortcuts import render,redirect
from ..models.forms import TarefaForm
from ..models.tarefa import TarefasModel
from django.http import HttpRequest

def home(request):
    contexto = {
        'nome': 'Pedro',
        'tarefas':TarefasModel.objects.all()
    }
    return render(request, 'home.html', contexto)


def adicionar_tarefa(request:HttpRequest):
    if request.method == 'POST':
        formulario = TarefaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('index')
    else:
        formulario = TarefaForm()

    contexto = {
        "form": formulario
    }
    return render(request, 'add.html', contexto)

