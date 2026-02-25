from django.shortcuts import render, redirect, get_object_or_404
from ..models.forms import TarefaForm
from ..models.tarefa import TarefasModel
from django.http import HttpRequest

def home(request):
    contexto = {
        'nome': 'Pedro',
        'tarefas': TarefasModel.objects.all()
    }
    return render(request, 'home.html', contexto)


def adicionar_tarefa(request: HttpRequest):
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


def editar_lista(request: HttpRequest):
    contexto = {
        'tarefas': TarefasModel.objects.all()
    }
    return render(request, 'editar_lista.html', contexto)


def editar_tarefa(request: HttpRequest, id: int):
    tarefa = get_object_or_404(TarefasModel, id=id)

    if request.method == 'POST':
        formulario = TarefaForm(request.POST, instance=tarefa)
        if formulario.is_valid():
            formulario.save()
            return redirect('index')
    else:
        formulario = TarefaForm(instance=tarefa)

    contexto = {
        'form': formulario,
        'tarefa': tarefa
    }
    return render(request, 'editar_form.html', contexto)
