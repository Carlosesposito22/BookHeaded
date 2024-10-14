from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Modalidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Clube(models.Model):
    id = models.AutoField(primary_key=True)
    moderador = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    modalidade = models.ForeignKey('Modalidade', on_delete=models.SET_NULL, null=True, blank=True, default='Sem modalidade')
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True, default='Sem categoria')
    descricao = models.TextField(null=True, blank=True)
    sobre = models.TextField(blank=True,null=True)
    numeroMembros = models.IntegerField(null=True, blank=True, default=1)
    privado = models.BooleanField(default=False)
    dataDeCriacao = models.DateTimeField(auto_now_add=True)
    progresso_atual = models.IntegerField(default=0)
    total_capitulos = models.IntegerField(default=50)
    favoritos = models.ManyToManyField(User, related_name='clubes_favoritos', blank=True)
    top_livros = models.TextField(blank=True, null=True)
    maratona_ativa = models.BooleanField(default=False)
    data_fim_maratona = models.DateField(null=True, blank=True)
    data_inicio_maratona = models.DateField(null=True, blank=True)
    capitulo_final_maratona = models.IntegerField(null=True, blank=True)
    capitulo_atual_maratona = models.IntegerField(null=True, blank=True)
    nome_maratona = models.CharField(max_length=100, null=True, blank=True)
    total_maratona_finalizadas = models.IntegerField(default=0)

    def calcular_progresso(self):
        return (self.progresso_atual / self.total_capitulos) * 100 if self.total_capitulos else 0
    
    def get_absolute_url(self):
        return reverse('club-Detail', args=[self.pk])

    def __str__(self):
        return f'{self.titulo} | {self.moderador} | {self.dataDeCriacao.strftime("%d/%m/%Y %H:%M")}'

    def get_absolute_url(self):
        return reverse('club-Detail', args=[str(self.id)])

    def total_avaliacoes(self):
        return self.avaliacao_set.count()
    
    def calcular_media_avaliacoes(self):
        avaliacoes = self.avaliacao_set.all()
        if avaliacoes.exists():
            total = sum(avaliacao.valor for avaliacao in avaliacoes)
            return total / avaliacoes.count()
        return 0
    
    def estrelas_avaliacoes(self):
        media = self.calcular_media_avaliacoes()
        estrelas_cheias = int(media) 
        estrelas_metade = 1 if media - estrelas_cheias >= 0.5 else 0 
        estrelas_vazias = 5 - (estrelas_cheias + estrelas_metade) 

        return (
            '<i class="bi bi-star-fill"></i>' * estrelas_cheias + 
            '<i class="bi bi-star-half"></i>' * estrelas_metade + 
            '<i class="bi bi-star"></i>' * estrelas_vazias
        )
    
    def contar_membros(self):
        return self.membros.filter(aprovado=True).count() + 1

class Avaliacao(models.Model):
    clube = models.ForeignKey(Clube, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.IntegerField()

    def __str__(self):
        return f'Avaliação de {self.usuario.username} para {self.clube.titulo} com valor {self.valor}'


class Membro(models.Model):
    clube = models.ForeignKey('Clube', on_delete=models.CASCADE, related_name="membros")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    dataDeEntrada = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=False)
    motivo_recusa = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.clube.titulo}"

User = get_user_model()

class Comentario(models.Model):
    clube = models.ForeignKey(Clube, related_name='comentarios', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.clube.titulo, self.user.username)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    seguindo = models.ManyToManyField(User, related_name='seguidores', blank=True)  
    icone = models.CharField(max_length=255, blank=True, null=True)  

    def __str__(self):
        return self.user.username
    
class HistoricoMaratona(models.Model):
    clube = models.ForeignKey(Clube, on_delete=models.CASCADE)
    nome_maratona = models.CharField(max_length=255)
    data_fim = models.DateField()
    data_inicio = models.DateField(null=True, blank=True)
    capitulo_final = models.CharField(max_length=255)
    capitulo_atual = models.CharField(max_length=255,null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_maratona} - {self.data_fim} - {self.data_inicio}"