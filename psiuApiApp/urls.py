from django.urls import path 
from psiuApiApp import views

app_name = 'psiuApiApp' 

urlpatterns = [ 
    path("lista/",  
         views.AtividadeListaView.as_view(),  
         name='lista-atividades'),
    path("lista/<str:tipo_atividade>/",  
         views.AtividadeListaTipoView.as_view(),  
         name='lista-atividades-tipo'), 
    path('uma_atividade/', views.AtividadeSingleView.as_view(), name='uma-atividade'),
    path('uma_atividade/<int:id_arg>/', views.AtividadeSingleIDView.as_view(), name='consulta-atividade'),  
        
     path('participa_atividade/', views.ParticipaAtividadeView.as_view(), name='participa-atividade'),
] 