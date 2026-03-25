from django.urls import path
from controller.home.home_controller import HomeController

urlpatterns = [
    path('', HomeController.index, name='home'),
    path('search/', HomeController.search, name='home_search'),
]
