from django.http import request
from django.shortcuts import render

class HomeController():
    @staticmethod
    def index():
        return render(request, 'index.html')