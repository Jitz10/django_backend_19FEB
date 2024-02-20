
from django.urls import path
from .views import form_handler, dashboard

urlpatterns = [
    path('form', form_handler, name='form_handler'),
    path('dashboard/<str:term>', dashboard, name='dashboard'),
]
