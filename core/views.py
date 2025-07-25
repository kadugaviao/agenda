from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
    evento = Evento.objects.filter(usuario=request.user)
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
        data_evento = request.POST.get('data_evento')
        local = request.POST.get('local')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        evento = Evento.objects.get(id=id_evento)
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()

            #Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #data_evento=data_evento,descricao=descricao)
        else:
            Evento.objects.create(
            titulo=titulo, 
            data_evento=data_evento, 
            local=local,
            descricao=descricao, 
            usuario=usuario)
        
    
    return redirect('/agenda/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')

