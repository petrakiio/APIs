from django.http import HttpResponse
from django.shortcuts import render

def teste(request):
    return HttpResponse('Olá')

def index(request):
    contexto = {
        "nome":"Pedro",
        "idade":"15",
    }
    return render(request,'home/home.html',contexto)
