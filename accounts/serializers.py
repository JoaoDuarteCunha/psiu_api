
from rest_framework import serializers 
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = User     # nome do modelo 
  fields = ['first_name', 'last_name', 'email'] # lista de campos 