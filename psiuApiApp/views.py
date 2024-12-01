from django.shortcuts import render
from django.utils.decorators import method_decorator

# Create your views here.
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.decorators import api_view, renderer_classes 
from rest_framework.renderers import JSONRenderer 
from psiuApiApp.serializers import AtividadeSerializer, CaronaSerializer, ConhecerPessoasSerializer, EstudosSerializer, ExtracurricularesSerializer, LigaSerializer, ParticipaAtividadeSerializer 
from psiuApiApp.models import Atividade, Carona, ConhecerPessoas, Estudos, Extracurriculares, Liga, ParticipaAtividade 
from rest_framework.authtoken.models import Token 

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

#Recebe string e retorna o serializer para cada tipo de atividade
tipo_atividade_serializer = {'carona': CaronaSerializer, 'estudos': EstudosSerializer, 'ligas': LigaSerializer, 'extracurriculares': ExtracurricularesSerializer, 'conhecer_pessoas': ConhecerPessoasSerializer}
#Recebe string e retorna o model para cada tipo de atividade
tipo_atividade_model = {'carona': Carona, 'estudos': Estudos, 'ligas': Liga, 'extracurriculares': Extracurriculares, 'conhecer_pessoas': ConhecerPessoas}


class AtividadeListaView(APIView): 
  '''
  Classe com operações para toda a lista de atividades, sem receber parâmetros

  Possiblita:
  - get: Lista todas as atividades
  - delete: Delete uma atividade
  '''   

  #Token de autenticação
  authentication_classes = [TokenAuthentication]

  #Autenticação necessária para todas as operações sem ser get
  def get_permissions(self):
      if self.request.method == 'GET':
          return [AllowAny()]
      else:
          return [IsAuthenticated()]

  #LISTA UMA ATIVIDADE/TODAS ATIVIDADES
  @swagger_auto_schema( 
    operation_summary='Lista todas as atividades', 
    operation_description="Obter informações sobre todas as atividades", 
    request_body=None,  # opcional 
    responses={200: AtividadeSerializer()} 
  )
  def get(self, request):
    ''' 
    Retorna uma lista de atividades

    Depende de: 
    - APIView 
    - Atividade 
    - AtividadeSerializer 
    - Response 

    :param APIView self: o próprio objeto 
    :param Request request: um objeto representando o pedido HTTP  
    :param HTTP: não tem 
    :return: uma lista de atividades em formato JSON 
    :rtype: JSON 
    '''
    queryset = Atividade.objects.all().order_by('id')
    serializer = AtividadeSerializer(queryset, many=True)
    return Response(serializer.data)

  @swagger_auto_schema(
      operation_summary='Remove uma atividade', 
      operation_description='Remove uma atividade', 
      request_body=openapi.Schema(
        type=openapi.TYPE_INTEGER,
        description='ID da atividade a ser removida'
      ),
      security=[{'Token':[]}], 
      manual_parameters=[ 
      openapi.Parameter('Authorization', openapi.IN_HEADER, 
      type=openapi.TYPE_STRING, default='token ', 
      description='Token de autenticação no formato "token \<<i>valor do token</i>\>"', 
      ), 
      ], 
      responses={ 
          204: AtividadeSerializer(),  
          404: None, 
      }, 
    ) 
  #REMOVE ATIVIDADE
  def delete(self, request): 
    ''' 
    Apaga uma atividade

    Depende de: 
    - APIView 
    - Atividade
    - AtividadeSerializer 
    - Response 

    :param APIView self: o próprio objeto 
    :param Request request: um objeto representando o pedido HTTP  
    :param HTTP: não tem
    :return: a atividade em formato JSON 
    :rtype: JSON 
    '''
    try: 
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] 
        token_obj = Token.objects.get(key=token) 
    except (Token.DoesNotExist, IndexError): 
        return Response({'msg': 'Token não existe.'}, status=status.HTTP_400_BAD_REQUEST) 
      
    atividade = Atividade.objects.get(id=request.data) 
    atividade_tipo = tipo_atividade_model[atividade.tipo_atividade].objects.get(id=request.data)
    if atividade.criador_id != token_obj.user.username: #Precisa ser o criador para apagar essa atividade
      return Response({'error': 'Somente o criador pode apagar a atividade.'},status.HTTP_401_UNAUTHORIZED) 

    if atividade and atividade_tipo: 
      atividade.delete()
      atividade_tipo.delete()
      return Response(status=status.HTTP_204_NO_CONTENT) 
    else: 
      return Response({'error': f'item [{request.data}] não encontrado'},status.HTTP_404_NOT_FOUND)


class AtividadeListaTipoView(APIView):
  @swagger_auto_schema( 
    operation_summary='Lista todas as atividades de um tipo', 
    operation_description="Obtem todas as atividades de um tipo específico", 
    responses={ 
      200: AtividadeSerializer(), 
      400: 'Mensagem de erro', 
      404: 'Tipo de atividade inválida', 
    }, 
    manual_parameters=[ 
      openapi.Parameter('tipo_atividade',openapi.IN_PATH, 
                        default='carona', 
                        type=openapi.TYPE_STRING, 
                        required=True, 
                        description='id da atividade na URL', 
      ), 
    ], 
  ) 
  def get(self, request, tipo_atividade: str):
    ''' 
    Retorna uma lista de atividades de um tipo especificado

    Depende de: 
    - APIView 
    - Atividade 
    - AtividadeSerializer 
    - Response 

    :param APIView self: o próprio objeto 
    :param Request request: um objeto representando o pedido HTTP  
    :param HTTP: não tem
    :param string tipo_atividade: o nome do tipo da atividade
    :return: uma lista de atividades em formato JSON 
    :rtype: JSON 
    '''
    tipo_atividade_model.get(tipo_atividade, None)
    if tipo_atividade is not None:
      queryset = tipo_atividade_model[tipo_atividade].objects.all().order_by('id')
      serializer = tipo_atividade_serializer[tipo_atividade](queryset, many=True)
      return Response(serializer.data)
    else:
      return Response(
          {'msg': f'Tipo de atividade #{tipo_atividade} nao existe'},
          status=status.HTTP_404_NOT_FOUND
      )
   


class AtividadeSingleIDView(APIView): 

  def singleAtividade(self, id_arg: int): 
    ''' 
    Retorna uma atividade com base no `id_arg`

    :param APIView self: o próprio objeto 
    :param int id_arg: o ID da atividade 
    :return: (o objetivo da atividade, o tipo da atividade)
    :rtype: tuple 
    ''' 
    try: 
      queryset = Atividade.objects.get(id=id_arg)
      tipo_atividade = queryset.tipo_atividade
      queryset = tipo_atividade_model[tipo_atividade].objects.get(id=id_arg)

      return queryset, tipo_atividade
    except Atividade.DoesNotExist: # id não existe 
      return None 
  
  #Token de autenticação
  authentication_classes = [TokenAuthentication]

  #Autenticação necessária para todas as operações sem ser get
  def get_permissions(self):
      if self.request.method == 'GET':
          return [AllowAny()]
      else:
          return [IsAuthenticated()]

  @swagger_auto_schema( 
    operation_summary='Dados de uma atividade', 
    operation_description="Obtem informações sobre uma atividade específica", 
    responses={ 
      200: AtividadeSerializer(), 
      400: 'Mensagem de erro', 
    }, 
    manual_parameters=[ 
      openapi.Parameter('id_arg',openapi.IN_PATH, 
                        default=5, 
                        type=openapi.TYPE_INTEGER, 
                        required=True, 
                        description='id da atividade na URL', 
      ), 
    ], 
  ) 
  def get(self, request, id_arg: int): 
    ''' 
    Retorna uma atividade e seus participantes

    Depende de: 
    - APIView 
    - Atividade
    - ParticipaAtividade
    - AtividadeSerializer 
    - ParticipaAtividadeSerializer 
    - Response 

    :param APIView self: o próprio objeto 
    :param Request request: um objeto representando o pedido HTTP  
    :param HTTP: não tem
    :param int id_arg: o id da atividade
    :return: a atividade e seus participantes em formato JSON 
    :rtype: JSON 
    '''
    queryset, tipo_atividade = self.singleAtividade(id_arg)
    if queryset:
      serializer = tipo_atividade_serializer[tipo_atividade](queryset) #Usa o serializer específico para o tipo selecionado
      queryset_participantes = ParticipaAtividade.objects.filter(atividade=serializer.data['id'])
      serializer_participantes = ParticipaAtividadeSerializer(queryset_participantes, many=True)
      return Response({'atividade': serializer.data, 'participantes': serializer_participantes.data}) #Retorna a atividade e seus participantes
    else:
      return Response(
          {'msg': f'Atividade com id #{id_arg} nao existe'},
          status=status.HTTP_404_NOT_FOUND
      )

  @swagger_auto_schema( 
    operation_summary='Atualiza atividade', operation_description="Atualizar uma atividade",
    security=[{'Token':[]}], 
    request_body=openapi.Schema( 
     type=openapi.TYPE_OBJECT, 
     properties={ 
      'adicionais': openapi.Schema(default='', description='Informações sobre a atividade', type=openapi.TYPE_STRING),
      'vagas': openapi.Schema(default=4, description='Vagas disponíveis para a atividade',  type=openapi.TYPE_INTEGER),
      'data': openapi.Schema(default='2024-12-25', description='Data da atividade', type=openapi.TYPE_STRING),
      'hora': openapi.Schema(default='22:45', description='Horário da atividade', type=openapi.TYPE_STRING),
      'tipo_atividade': openapi.Schema(default='carona', description='Tipo da atividade', type=openapi.TYPE_STRING),
     }, 
    ), 
    responses={200: AtividadeSerializer(), 400: AtividadeSerializer(), }, 
    manual_parameters=[
    openapi.Parameter('Authorization', openapi.IN_HEADER, 
     type=openapi.TYPE_STRING, default='token ', 
     description='Token de autenticação no formato "token \<<i>valor do token</i>\>"', 
     ),  
     openapi.Parameter('id_arg',openapi.IN_PATH, default=41, type=openapi.TYPE_INTEGER,  
                       required=True, description='id da atividade na URL',),], 
  )  
  def put(self, request, id_arg):
    ''' 
    Atualiza uma atividade

    Depende de: 
    - APIView 
    - Atividade
    - AtividadeSerializer 
    - Response 

    :param APIView self: o próprio objeto 
    :param Request request: um objeto representando o pedido HTTP  
    :param HTTP: não tem
    :param int id_arg: o id da atividade
    :return: a atividade em formato JSON 
    :rtype: JSON 
    '''
    atividade, tipo_atividade = self.singleAtividade(id_arg) #Recebe a atividade e o tipo dela
    data = request.data
    data['criador_id'] = atividade.criador_id #Preenche o criador
    data['tipo_atividade'] = atividade.tipo_atividade #Preenche o tipo de atividade
    serializer = tipo_atividade_serializer[tipo_atividade](atividade,  #Usa o serializer específico para o tipo de atividade
                                  data=data) 
    if serializer.is_valid(): #Se atividade for válida, retorna
      serializer.save() 
      return Response(serializer.data,  
                      status.HTTP_200_OK) 
    else: 
      print(serializer.errors)
      return Response(serializer.errors,  
                      status.HTTP_400_BAD_REQUEST) 

class AtividadeSingleView(APIView):

  authentication_classes = [TokenAuthentication]

  #Autenticação sempre necessária para os métodos dessa classe
  def get_permissions(self):
          return [IsAuthenticated()]

  @swagger_auto_schema( 
    operation_summary='Cria atividade', operation_description="Cria uma atividade nova. Precisa do token do usuário para armazená-lo como usuario_id", 
    security=[{'Token':[]}], 
    manual_parameters=[ 
        openapi.Parameter( 
        'Authorization', 
        openapi.IN_HEADER, 
        type=openapi.TYPE_STRING, 
        description='Token de autenticação no formato "token \<<i>valor do token</i>\>"', 
        default='token ', 
        ), 
    ], 
    request_body=openapi.Schema( 
     type=openapi.TYPE_OBJECT, 
     properties={ 
      'adicionais': openapi.Schema(default='', description='Informações sobre a atividade', type=openapi.TYPE_STRING),
      'vagas': openapi.Schema(default=4, description='Vagas disponíveis para a atividade',  type=openapi.TYPE_INTEGER),
      'data': openapi.Schema(default='2024-12-25', description='Data da atividade', type=openapi.TYPE_STRING),
      'hora': openapi.Schema(default='22:45', description='Horário da atividade', type=openapi.TYPE_STRING),
      'tipo_atividade': openapi.Schema(default='carona', description='Tipo da atividade', type=openapi.TYPE_STRING),
     }, 
    ), 
    responses={200: AtividadeSerializer(), 400: 'Dados errados', }, 
  )  
  def post(self, request):
      ''' 
      Cria uma nova uma atividade

      Depende de: 
      - APIView 
      - Atividade
      - AtividadeSerializer 
      - Response 

      :param APIView self: o próprio objeto 
      :param Request request: um objeto representando o pedido HTTP  
      :param HTTP: não tem
      :return: a atividade em formato JSON 
      :rtype: JSON 
      '''
      tipo_serializer = tipo_atividade_serializer.get(request.data.get('tipo_atividade', None))
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


class ParticipaAtividadeView(APIView):


  @swagger_auto_schema( 
    operation_summary='Adiciona participante à atividade', operation_description="Adiciona/Remove usuário como participante de uma certa atividade. Se usuário ainda não participa da atividade, o adiciona. Se já participa, remove.", 
    request_body=openapi.Schema( 
     type=openapi.TYPE_OBJECT, 
     properties={ 
      'atividade': openapi.Schema(default=5, description='ID da atividade', type=openapi.TYPE_INTEGER),
      'usuario': openapi.Schema(default='visitante', description='Nome do participante',  type=openapi.TYPE_STRING),
     }, 
    ),
    security=[{'Token':[]}], 
    manual_parameters=[ 
    openapi.Parameter('Authorization', openapi.IN_HEADER, 
    type=openapi.TYPE_STRING, default='token ', 
    description='Token de autenticação no formato "token \<<i>valor do token</i>\>"', 
    ), 
    ], 
    responses={201: ParticipaAtividadeSerializer(), 200: 'Participação cancelada', 400: 'Token inválido', 401: 'Usuário não pode participar.'}, 
  )  
  def post(self, request):
      ''' 
      Adiciona participante a uma atividade

      Depende de: 
      - APIView 
      - Atividade
      - AtividadeSerializer 
      - ParticipaAtividade
      - Response 

      :param APIView self: o próprio objeto 
      :param Request request: um objeto representando o pedido HTTP  
      :param HTTP: não tem
      :return: a participação em formato JSON 
      :rtype: JSON 
      '''
      try: 
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] 
        token_obj = Token.objects.get(key=token) 
      except (Token.DoesNotExist, IndexError): 
          return Response({'msg': 'Token não existe.'}, status=status.HTTP_400_BAD_REQUEST) 
      
      atividade = Atividade.objects.get(id=request.data['atividade'])
      if atividade.criador_id == token_obj.user.username:
         return Response({'msg': 'O criador não pode participar de sua própria atividade'}, status=status.HTTP_401_UNAUTHORIZED)
      
      usuario_participa = ParticipaAtividade.objects.filter(atividade=request.data['atividade'], usuario=token_obj.user.username) 
      if len(usuario_participa) == 0: #Se o usuário ainda não participa
        if atividade.vagas > 0: #Se a atividade ainda tem vagas
          data=request.data
          data['usuario'] = token_obj.user.username
          atividade.vagas -= 1
          atividade.save() #Atualiza vagas da atividade

          serializer = ParticipaAtividadeSerializer(data=data) #Adiciona participação
          if serializer.is_valid():
              serializer.save() 
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          else:
              print(serializer.errors)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'Atividade sem vagas'}, status=status.HTTP_401_UNAUTHORIZED)
      else: #Se o usuário já participa da atividade
         atividade.vagas += len(usuario_participa) #Atualiza vagas
         atividade.save()

         for participante in usuario_participa: #Retira ele da atividade
            participante.delete()
        
      return Response({'msg': 'OK'}, status=status.HTTP_200_OK)
