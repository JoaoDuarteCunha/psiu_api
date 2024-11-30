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
            token = request.META.get('HTTP_AUTHORIZATION')
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
            print(request.META.get('HTTP_AUTHORIZATION'))
            token = request.META.get('HTTP_AUTHORIZATION')
            token_obj = Token.objects.get(key=token) 
            user = token_obj.user 

            return Response( 
            {'username': user.username},  
            status=status.HTTP_200_OK) 
        except (Token.DoesNotExist, AttributeError): 
            return Response( 
            {'username': 'visitante'},  
            status=status.HTTP_404_NOT_FOUND) 