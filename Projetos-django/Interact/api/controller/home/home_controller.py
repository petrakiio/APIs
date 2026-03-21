from django.shortcuts import render

class HomeController:
    @staticmethod
    def index(request):
        return render(request, 'index.html')
