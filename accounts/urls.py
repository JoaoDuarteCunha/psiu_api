from django.urls import path 
from accounts import views 
from django.urls import include 

app_name = 'accounts' 

urlpatterns = [
path('registro/', views.RegistroView.as_view(), name='registro'),
path('token-auth/', views.CustomAuthToken.as_view(), name='token-auth'), 
]