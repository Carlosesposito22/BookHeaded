from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date


class Categoria(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

class Modalidade(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

class Clube(models.Model):
    id = models.AutoField(primary_key=True)
    moderador = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    modalidade = models.ForeignKey('Modalidade', on_delete=models.SET_NULL,default='Sem modalidade',null=True, blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True,default='Sem categoria')
    descricao = models.TextField(null=True, blank=True)
    avaliacoes = models.IntegerField(null=True, blank=True, default=0)
    livroAtual = models.CharField(max_length=255, null=True, blank=True, default='Sem livro definido')
    numeroMembros = models.IntegerField(null=True, blank=True, default=1)
    privado = models.BooleanField(default=False)
    favoritado = models.BooleanField(default=False)
    dataDeCriacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} | {self.moderador} | {self.dataDeCriacao.strftime("%d/%m/%Y %H:%M")}'

    def get_absolute_url(self):
        return reverse('club-Detail', args=(str(self.id)))



