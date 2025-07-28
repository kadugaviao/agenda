from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    local = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        local_dt = timezone.localtime(self.data_evento)
        return local_dt.strftime('%d/%m/%Y %H:%M')

    def get_data_input_evento(self):
        local_dt = timezone.localtime(self.data_evento)
        return local_dt.strftime('%Y-%m-%dT%H:%M')
    
    def get_evento_atrasado(self):
        if self.data_evento < timezone.now():
            return True
        else: 
            return False