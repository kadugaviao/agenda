from django.shortcuts import render
from django.http import HttpResponse
from .models import Evento

def get_local_evento(request, titulo_evento):
    try:
        evento = Evento.objects.get(titulo=titulo_evento)
        return HttpResponse(evento.local)
    except Evento.DoesNotExist:
        return HttpResponse("Evento não encontrado", status=404)

# def index(request):
#   return redirect('/agenda/')

def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.all()
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

