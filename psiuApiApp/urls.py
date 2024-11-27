from django.urls import path 
from psiuApiApp import views

app_name = 'psiuApiApp' 

urlpatterns = [ 
    path("lista/",  
         views.AtividadeView.as_view(),  
         name='lista-atividades'), 
    path('uma_atividade/', views.AtividadeView.as_view(), name='uma-atividade'),
    path('uma_atividade/<int:id_arg>/', views.AtividadeView.as_view(), name='consulta-atividade'),  
] 