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

