from django.urls import path
from controller.login.login_controller import LoginController


urlpatterns = [
    path('login/', LoginController.login, name='login'),
    path('cadastro/', LoginController.signup, name='signup'),
    path('logout/',LoginController.logout,name='logout')
]
