from django.shortcuts import render
from django.utils.decorators import method_decorator

# Create your views here.
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.decorators import api_view, renderer_classes 
from rest_framework.renderers import JSONRenderer 
from psiuApiApp.serializers import AtividadeSerializer, CaronaSerializer, ConhecerPessoasSerializer, EstudosSerializer, ExtracurricularesSerializer, LigaSerializer 
from psiuApiApp.models import Atividade, Carona, ConhecerPessoas, Estudos, Extracurriculares, Liga 
from rest_framework.authtoken.models import Token 

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

class AtividadeView(APIView): 

  tipo_atividade_serializer = {'carona': CaronaSerializer, 'estudos': EstudosSerializer, 'ligas': LigaSerializer, 'extracurriculares': ExtracurricularesSerializer, 'conhecer_pessoas': ConhecerPessoasSerializer}
  tipo_atividade_model = {'carona': Carona, 'estudos': Estudos, 'ligas': Liga, 'extracurriculares': Extracurriculares, 'conhecer_pessoas': ConhecerPessoas}

  authentication_classes = [TokenAuthentication]

  def get_permissions(self):
      if self.request.method == 'GET':
          return [AllowAny()]
      else:
          return [IsAuthenticated()]
    
  def post(self, request):
      tipo_serializer = self.tipo_atividade_serializer.get(request.data.get('tipo_atividade', None))
      if tipo_serializer is not None:
          
          try: 
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] 
            token_obj = Token.objects.get(key=token) 
          except (Token.DoesNotExist, IndexError): 
              return Response({'msg': 'Token não existe.'}, status=status.HTTP_400_BAD_REQUEST) 
          
          data=request.data
          data['criador_id'] = token_obj.user.username
          serializer = tipo_serializer(data=data)
          if serializer.is_valid():
              serializer.save() 
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          else:
              print(serializer.errors)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      else:
          return Response(
              {"detail": "Tipo de atividade inválido! Especifique com o campo 'tipo_atividade'."},
              status=status.HTTP_400_BAD_REQUEST
          )
    
  def singleAtividade(self, id_arg): 
    try: 
      queryset = Atividade.objects.get(id=id_arg)
      tipo_atividade = queryset.tipo_atividade
      queryset = self.tipo_atividade_model['tipo_atividade'].objects.get(id=id_arg)

      return queryset, tipo_atividade
    except Atividade.DoesNotExist: # id não existe 
      return None 
    
  #LISTA UMA ATIVIDADE/TODAS ATIVIDADES
  @swagger_auto_schema( 
    operation_summary='Lista todos os carros', 
    operation_description="Obter informações sobre todos os carros", 
    request_body=None,  # opcional 
    responses={200: AtividadeSerializer()} 
  ) 
  def get(self, request, id_arg=None, tipo_atividade=None): 
    if id_arg is not None:
      queryset, tipo_atividade = self.singleAtividade(id_arg)
      if queryset:
          serializer = self.tipo_atividade_serializer[tipo_atividade](queryset)
          return Response(serializer.data)
      else:
          return Response(
              {'msg': f'Atividade com id #{id_arg} nao existe'},
              status=status.HTTP_404_NOT_FOUND
          )
    else:
      if tipo_atividade is not None:
        queryset = self.tipo_atividade_model[tipo_atividade].objects.all().order_by('id')
        serializer = self.tipo_atividade_serializer[tipo_atividade](queryset, many=True)
        return Response(serializer.data)
      else:
        queryset = Atividade.objects.all().order_by('id')
        serializer = AtividadeSerializer(queryset, many=True)
        return Response(serializer.data)
    
  #ATUALIZA ATIVIDADE
  def put(self, request, id_arg): 
    atividade = self.singleAtividade(id_arg) 
    serializer = AtividadeSerializer(atividade,  
                                  data=request.data) 
    if serializer.is_valid(): 
      serializer.save() 
      return Response(serializer.data,  
                      status.HTTP_200_OK) 
    else: 
      return Response(serializer.errors,  
                      status.HTTP_400_BAD_REQUEST) 
    
  #REMOVE ATIVIDADE
  def delete(self, request): 
    id_erro = "" 
    erro = False 
    for id in request.data: 
      atividade = Atividade.objects.get(id=id) 
      if atividade: 
        atividade.delete() 
      else: 
        id_erro += str(id) 
        erro = True 
    if erro: 
      return Response({'error': f'item [{id_erro}] não encontrado'},status.HTTP_404_NOT_FOUND) 
    else: 
      return Response(status=status.HTTP_204_NO_CONTENT) 