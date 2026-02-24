from django.http import HttpResponse

def teste(request):
    return HttpResponse('Olá')

def index(request):
    return HttpResponse('Ola visitante')