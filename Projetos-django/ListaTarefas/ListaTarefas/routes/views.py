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

def remover_tarefa(request: HttpRequest):
    if request.method == 'POST':
        tarefa_id = request.POST.get('tarefa_id')
        if tarefa_id:
            TarefasModel.objects.filter(id=tarefa_id).delete()
        return redirect('remover')

    contexto = {
        'tarefas': TarefasModel.objects.all()
    }
    return render(request, 'remover.html', contexto)
