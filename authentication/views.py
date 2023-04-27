from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import validate_fields, validate_password
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login as logar, logout

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/eventos/novo_evento/')
        
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect(reverse('login'))
        
        logar(request, user)
        return redirect('/eventos/novo_evento/')

def register(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/eventos/novo_evento/')

        return render(request, 'register.html')
    elif request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not validate_fields(username, email, password, confirmar_senha):
            messages.add_message(request, constants.ERROR, 'Campos inválidos')
            return redirect(reverse('register'))
        
        if not validate_password(request, password, confirmar_senha):   
            return redirect(reverse('register'))

        if User.objects.filter(username=username).exists():
            return redirect(reverse('register'))  

        try: 
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso.')
            return redirect(reverse('login'))
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
            return redirect(reverse('register'))

def exit(request):
    logout(request)
    return redirect(reverse('login'))