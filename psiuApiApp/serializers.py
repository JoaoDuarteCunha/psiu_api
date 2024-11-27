
from rest_framework import serializers 
from psiuApiApp.models import Atividade 
 
class AtividadeSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = Atividade     # nome do modelo 
  fields = '__all__' # lista de campos 