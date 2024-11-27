from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.decorators import api_view, renderer_classes 
from rest_framework.renderers import JSONRenderer 
from psiuApiApp.serializers import AtividadeSerializer 
from psiuApiApp.models import Atividade 

from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

class AtividadeView(APIView): 


  #INSERE UMA ATIVIDADE
  def post(self, request): 
        serializer = AtividadeSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data,  
                            status.HTTP_201_CREATED) 
        else: 
            return Response(serializer.errors,  
                            status.HTTP_400_BAD_REQUEST)
    
  def singleAtividade(self, id_arg): 
    try: 
      queryset = Atividade.objects.get(id=id_arg) 
      return queryset 
    except Atividade.DoesNotExist: # id não existe 
      return None 
    
  #LISTA UMA ATIVIDADE/TODAS ATIVIDADES
  @swagger_auto_schema( 
    operation_summary='Lista todos os carros', 
    operation_description="Obter informações sobre todos os carros", 
    request_body=None,  # opcional 
    responses={200: AtividadeSerializer()} 
  ) 
  def get(self, request, id_arg=None): 
    if id_arg is not None:
      queryset = self.singleAtividade(id_arg)
      if queryset:
          serializer = AtividadeSerializer(queryset)
          return Response(serializer.data)
      else:
          return Response(
              {'msg': f'Atividade com id #{id_arg} nao existe'},
              status=status.HTTP_404_NOT_FOUND
          )
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