
from rest_framework import serializers 
from psiuApiApp.models import Atividade, Carona, ConhecerPessoas, Estudos, Extracurriculares, Liga, ParticipaAtividade 
 
class AtividadeSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = Atividade     # nome do modelo 
  fields = '__all__' # lista de campos 

class CaronaSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = Carona     # nome do modelo 
  fields = '__all__' # lista de campos 

class ExtracurricularesSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = Extracurriculares     # nome do modelo 
  fields = '__all__' # lista de campos 

class EstudosSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = Estudos     # nome do modelo 
  fields = '__all__' # lista de campos 

class LigaSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = Liga     # nome do modelo 
  fields = '__all__' # lista de campos 

class ConhecerPessoasSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = ConhecerPessoas     # nome do modelo 
  fields = '__all__' # lista de campos 

class ParticipaAtividadeSerializer(serializers.ModelSerializer): 
 class Meta: 
  model = ParticipaAtividade     # nome do modelo 
  fields = '__all__' # lista de campos 