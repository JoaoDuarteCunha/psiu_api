from django.urls import path 
from accounts import views 
from django.urls import include 

app_name = 'accounts' 

urlpatterns = [
path('perfil/<str:nome_usuario>/', views.PerfilView.as_view(), name='perfil'),
path('perfil/', views.PerfilEditView.as_view(), name='perfil-edit'),
path('registro/', views.RegistroView.as_view(), name='registro'),
path('token-auth/', views.CustomAuthToken.as_view(), name='token-auth'), 
path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')), 
]