
from rest_framework import serializers 
from psiuApiApp.models import Atividade, Carona 
 
class AtividadeSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = Atividade     # nome do modelo 
  fields = '__all__' # lista de campos 

class CaronaSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = Carona     # nome do modelo 
  fields = '__all__' # lista de campos 