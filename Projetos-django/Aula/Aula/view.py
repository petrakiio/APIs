from django.http import HttpResponse
from django.shortcuts import render

def teste(request):
    return HttpResponse('Olá')

def index(request):
    contexto = {
        "Nome":"Pedro",
        "Idade":"15",
    }
    return render(request,'home/home.html')
