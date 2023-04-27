from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from secrets import token_urlsafe
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO  
from .utils import validate_fields
from .models import Evento, Certificado
import sys
import csv
import os

@login_required(login_url='/auth/login/')
def novo_evento(request):

    if request.method == "GET":
        return render(request, 'novo_evento.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')
        
        logo = request.FILES.get('logo')
        
        if not validate_fields(nome, descricao, data_inicio, data_termino, carga_horaria):
            messages.add_message(request, constants.ERROR, 'Campos inválidos.')
            return redirect(reverse('novo_evento'))

        if not logo != None:
            messages.add_message(request, constants.ERROR, 'Nenhuma imagem detectada!')
            return redirect(reverse('novo_evento'))

        evento = Evento(
            criador=request.user,
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            carga_horaria=carga_horaria,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
            logo=logo,
        )
    
        evento.save()
        
        messages.add_message(request, constants.SUCCESS, 'Evento cadastrado com sucesso')
        return redirect(reverse('novo_evento'))

@login_required(login_url='/auth/login/')   
def gerenciar_evento(request):
    if request.method == "GET":

        nome_evento = request.GET.get('nome')

        eventos = Evento.objects.all()

        if nome_evento:
            eventos = Evento.objects.filter(nome__icontains=nome_evento)

        context = {
            'eventos': eventos,
        }

        return render(request, 'gerenciar_evento.html', context=context)
    
@login_required(login_url='/auth/login/')
def meus_eventos(request):
    if request.method == "GET":

        nome_evento = request.GET.get('nome')

        eventos = Evento.objects.filter(criador=request.user)

        if nome_evento:
            eventos = Evento.objects.filter(nome__icontains=nome_evento)

        context = {
            'eventos': eventos,
        }

        return render(request, 'meus_eventos.html', context=context)

@login_required(login_url='/auth/login/')
def inscrever_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    user = request.user
    if request.method == "GET":
        return render(request, 'inscrever_evento.html', {'evento': evento})
    
    elif request.method == 'POST':
        if not user in evento.participantes.all():
            evento.participantes.add(user)
            evento.save()

            messages.add_message(request, constants.SUCCESS, 'Inscrição realizada com sucesso!')
            return redirect(f'/eventos/inscrever_evento/{evento.id}')
        else:
            evento.participantes.remove(user)
            messages.add_message(request, constants.WARNING, 'Você não está mais participando desse evento!')
            return redirect(f'/eventos/inscrever_evento/{evento.id}')
        
@login_required(login_url='/auth/login/')
def participantes_evento(request, id):
    evento = get_object_or_404(Evento, id=id)

    if not evento.criador == request.user:
        raise Http404('Erro interno do sistema.')
    
    if request.method == "GET":
        participantes = evento.participantes.all()
        return render(request, 'participantes_evento.html', {'evento': evento, 'participantes': participantes})

@login_required(login_url='/auth/login/')
def gerar_csv(request, id):
    evento = get_object_or_404(Evento, id=id)

    if not evento.criador == request.user:
        raise Http404('Erro interno do sistema.')
    
    participantes = evento.participantes.all()

    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    with open(path, 'w') as arq:
        writer = csv.writer(arq, delimiter='|')
        for participante in participantes:
            x = (participante.username, participante.email)
            writer.writerow(x)

    return redirect(f'/media/{token}')

@login_required(login_url='/auth/login/')
def certificados_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Erro interno do sistema')
    if request.method == "GET":
        qtd_certificados = evento.participantes.all().count() - Certificado.objects.filter(evento=evento).count()
        return render(request, 'certificados_evento.html', {'evento': evento, 'qtd_certificados': qtd_certificados})

@login_required(login_url='/auth/login/')
def gerar_certificado(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Erro interno do sistema!')

    path_template = os.path.join(settings.BASE_DIR, 'templates/static/evento/img/template_certificado.png')
    path_fonte = os.path.join(settings.BASE_DIR, 'templates/static/font/arimo.ttf')
    for participante in evento.participantes.all():
        # TODO: Validar se já existe certificado desse participante para esse evento
        img = Image.open(path_template)
        path_template = os.path.join(settings.BASE_DIR, 'templates/static/evento/img/template_certificado.png')
        draw = ImageDraw.Draw(img)
        fonte_nome = ImageFont.truetype(path_fonte, 60)
        fonte_info = ImageFont.truetype(path_fonte, 30)
        draw.text((225, 641), f"{participante.username}", font=fonte_nome, fill=(0, 0, 0))
        draw.text((761, 769), f"{evento.nome}", font=fonte_info, fill=(0, 0, 0))
        draw.text((816, 838), f"{evento.carga_horaria} horas", font=fonte_info, fill=(0, 0, 0))
        output = BytesIO()
        img.save(output, format="PNG", quality=100)
        output.seek(0)
        img_final = InMemoryUploadedFile(output,
                                        'ImageField',
                                        f'{token_urlsafe(8)}.png',
                                        'image/jpeg',
                                        sys.getsizeof(output),
                                        None)
        certificado_gerado = Certificado(
            certificado=img_final,
            participante=participante,
            evento=evento,
        )
        certificado_gerado.save()

        

    messages.add_message(request, constants.SUCCESS, 'Certificados gerados')
    return redirect(reverse('certificados_evento', kwargs={'id': evento.id}))

@login_required(login_url='/auth/login/')
def procurar_certificado(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Eroo interno do sistema')
    email = request.POST.get('email')
    certificado = Certificado.objects.filter(evento=evento).filter(participante__email=email).first()
    if not certificado:
        messages.add_message(request, constants.WARNING, 'Certificado não encontrado')
        return redirect(reverse('certificados_evento', kwargs={'id': evento.id}))
    
    return redirect(certificado.certificado.url)