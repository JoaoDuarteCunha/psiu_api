from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from rest_framework.response import Response 
from rest_framework import status 
# Autenticação 
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

# Swagger 
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import UserCreationForm

class RegistroView(APIView):
    def post(self, request):
        formulario = UserCreationForm(request.data) 
        if formulario.is_valid():
            senha = formulario.cleaned_data.get('password1')
            username = formulario.save()
            user = authenticate(request, username=username, password=senha)
            if user is not None: 
                token, _ = Token.objects.get_or_create(user=user) 
                login(request, user) 
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            return Response({'msg': 'Ocorreu uma falha.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                {'msg': 'Formulário inválido.', 'errors': formulario.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class PerfilView(APIView):
    '''Recebe o nome de usuário e retorna o id do usuário'''
    def get(self, request, nome_usuario):
        try:
            usuario = User.objects.get(username=nome_usuario)
            return Response( 
                {'id': usuario.id},  
                status=status.HTTP_200_OK) 
        except:
            return Response( 
            {'id': -1},  
            status=status.HTTP_404_NOT_FOUND) 




class CustomAuthToken(ObtainAuthToken): 
    @swagger_auto_schema( 
        operation_summary='Obtém o username do usuário', 
        operation_description="Retorna o username do usuário ou apenas visitante se o usuário não possui conta",
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
        responses={ 
            200: openapi.Response( 
                description='Nome do usuário', 
                schema=openapi.Schema( 
                    type=openapi.TYPE_OBJECT, 
                    properties={'username': openapi.Schema(type=openapi.TYPE_STRING)}, 
                ), 
            ) 
        },
    )
    def post(self, request, *args, **kwargs): 
        serializer = self.serializer_class(data=request.data, context={'request': request}) 
        if serializer.is_valid(): 
            username = serializer.validated_data['username'] 
            password = serializer.validated_data['password']  
            user = authenticate(request, username=username, password=password) 
            if user is not None: 
                token, _ = Token.objects.get_or_create(user=user) 
                login(request, user) 
                return Response({'token': token.key}) 
            return Response(status=status.HTTP_401_UNAUTHORIZED) 

    

    @swagger_auto_schema( 
        operation_description='Realiza logout do usuário, apagando o seu token', 
        operation_summary='Realiza logout', 
        security=[{'Token':[]}], 
        manual_parameters=[ 
        openapi.Parameter('Authorization', openapi.IN_HEADER, 
        type=openapi.TYPE_STRING, default='token ', 
        description='Token de autenticação no formato "token \<<i>valor do token</i>\>"', 
        ), 
        ], 
        request_body=None, 
        responses={ 
            status.HTTP_200_OK: 'User logged out', 
            status.HTTP_400_BAD_REQUEST: 'Bad request', 
            status.HTTP_401_UNAUTHORIZED: 'User not authenticated', 
            status.HTTP_403_FORBIDDEN: 'User not authorized to logout', 
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Erro no servidor', 
        }, 
    )
    def delete(self, request): 
        try: 
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] 
            token_obj = Token.objects.get(key=token) 
        except (Token.DoesNotExist, IndexError): 
            return Response({'msg': 'Token não existe.'}, status=status.HTTP_400_BAD_REQUEST) 
        user = token_obj.user 
        if user.is_authenticated: 
            request.user = user 
            logout(request) 
            token = Token.objects.get(user=user) 
            token.delete() 
            return Response({'msg': 'Logout bem-sucedido.'},  
            status=status.HTTP_200_OK) 
        else: 
            return Response({'msg': 'Usuário não autenticado.'},  
            status=status.HTTP_403_FORBIDDEN) 


    def get(self, request): 
        ''' 
        Parâmetros: o token de acesso 
        Retorna: o username ou 'visitante' 
        ''' 
        try: 
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] 
            token_obj = Token.objects.get(key=token) 
            user = token_obj.user 

            return Response( 
            {'username': user.username},  
            status=status.HTTP_200_OK) 
        except (Token.DoesNotExist, AttributeError): 
            return Response( 
            {'username': 'visitante'},  
            status=status.HTTP_404_NOT_FOUND) 
        
    
    @swagger_auto_schema( 
        operation_description='Troca a senha do usuário, atualiza o token em caso de sucesso', 
        operation_summary='Troca a senha do usuário', 
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
                'old_password': openapi.Schema(type=openapi.TYPE_STRING), 
                'new_password1': openapi.Schema(type=openapi.TYPE_STRING), 
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING), 
            }, 
            required=['old_password', 'new_password1', 'new_password2'], 
        ), 
        responses={ 
            status.HTTP_200_OK: openapi.Response( 
                description="Senha alterada com sucesso.", 
                examples={ "application/json": { "message": "Senha alterada com sucesso." } } 
            ), 
            status.HTTP_400_BAD_REQUEST: openapi.Response( 
                description="Erro na solicitação.", 
                examples={ "application/json": { "old_password": ["Senha atual incorreta."] } } 
            ), 
        },)
    def put(self, request): 
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]    # token 
        token_obj = Token.objects.get(key=token) 
        user = token_obj.user 
        oldPassword = request.data.get('old_password') 
        newPassword = request.data.get('new_password1') 
        confirmPassword = request.data.get('new_password2') 
 
        if newPassword != confirmPassword: 
            return Response({'error': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST) 

        # Verificar se a senha atual está correta 
        if user.check_password(oldPassword): 
            # Alterar a senha e atualizar o token 
            user.set_password(newPassword) 
            user.save() 
             
            # Atualizar token 
            try: 
                token = Token.objects.get(user=user) 
                token.delete() 
                token, _ = Token.objects.get_or_create(user=user) 
            except Token.DoesNotExist: 
                pass 
            return Response({'token': token.key, "message": "Senha alterada com sucesso."},  
                            status=status.HTTP_200_OK) 
        else: 
            return Response({"old_password": ["Senha atual incorreta."]}, status=status.HTTP_400_BAD_REQUEST) 