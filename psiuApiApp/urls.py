from django.urls import path 
from psiuApiApp import views

app_name = 'psiuApiApp' 

urlpatterns = [ 
    path("lista/",  
         views.AtividadeView.as_view(),  
         name='lista-atividades'),
    path("lista/<str:tipo_atividade>/",  
         views.AtividadeView.as_view(),  
         name='lista-atividades-tipo'), 
    path('uma_atividade/', views.AtividadeView.as_view(), name='uma-atividade'),
    path('uma_atividade/<int:id_arg>/', views.AtividadeView.as_view(), name='consulta-atividade'),  
    path('participa_atividade/', views.ParticipaAtividadeView.as_view(), name='participa-atividade'),
    path('participa_atividade/<int:id_arg>/', views.ParticipaAtividadeView.as_view(), name='consulta-participantes'), 
    path('participa_atividade/<str:nome_usuario>/', views.ParticipaAtividadeView.as_view(), name='consulta-atividades-usuario'), 
] 