from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.conf import settings
from pytz import timezone as pytz_timezone
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User


from .models import Evento

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/') 

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username,password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return redirect('/')

def get_local_evento(request, titulo_evento):
    try:
        evento = Evento.objects.get(titulo=titulo_evento)
        return HttpResponse(evento.local)
    except Evento.DoesNotExist:
        return HttpResponse("Evento não encontrado", status=404)

# def index(request):
#   return redirect('/agenda/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = timezone.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual).order_by('data_evento')
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')

        data_evento_str = request.POST.get('data_evento')  
        fuso_brasilia = pytz_timezone('America/Sao_Paulo')
        data_evento = datetime.strptime(data_evento_str, "%Y-%m-%dT%H:%M")
        data_evento = fuso_brasilia.localize(data_evento)

        local = request.POST.get('local')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.local = local
                evento.save()
        else:
            Evento.objects.create(
                titulo=titulo,
                data_evento=data_evento,
                local=local,
                descricao=descricao,
                usuario=usuario
        )

    return redirect('/agenda/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except:  
        raise Http404
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404("Evento não encontrado")
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_evento(request, id_usuario):
    try:
        usuario = User.objects.get(id=id_usuario)
        evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
        return JsonResponse(list(evento), safe=False)
    except User.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado'}, status=404)
