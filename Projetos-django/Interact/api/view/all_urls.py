from django.urls import include, path

urlpatterns = [
    path('', include('view.home_urls')),
    path('', include('view.login_urls')),
]
