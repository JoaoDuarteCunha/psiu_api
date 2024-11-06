from django.urls import path 
from psiuApiApp import views

app_name = 'psiuApiApp' 

urlpatterns = [ 
    path('exemploClasse/', views.ExemploClasse.as_view(), name='exemploClasse'), 
    path('exemploGET/', views.exemploGET, name='exemploGET'), 
    path('exemploPOST/', views.exemploPOST, name='exemploPOST'), 
] 