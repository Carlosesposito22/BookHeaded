from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Profile
from .models import Clube, Membro, Comentario, Modalidade, Categoria 
from django.contrib.auth.models import User
from .views import comentario_create_view
from unittest.mock import patch
from django.test import Client
from .models import Modalidade
from django.conf import settings
import os
from django.http import HttpResponseForbidden


class SeguirUsuarioTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='senha123')
        self.user2 = User.objects.create_user(username='user2', password='senha123')

        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

    def test_seguir_usuario(self):
        self.client.login(username='user1', password='senha123')

        url = reverse('seguir_usuario', args=[self.user2.id])
        response = self.client.post(url)

        self.profile2.refresh_from_db()
        self.assertIn(self.user1, self.profile2.seguidores.all())

    def test_parar_seguir_usuario(self):

        self.client.login(username='user1', password='senha123')

        self.profile2.seguidores.add(self.user1)

        url = reverse('seguir_usuario', args=[self.user2.id])
        response = self.client.post(url)

        self.profile2.refresh_from_db()
        self.assertNotIn(self.user1, self.profile2.seguidores.all())

# Testes pros comentários:

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Clube, Comentario, Categoria

class ComentarioTestCase(TestCase):

    def setUp(self):
        # Cria um usuário para o teste
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Cria uma categoria válida para o clube
        self.categoria = Categoria.objects.create(nome="Sem categoria")

        # Cria um clube para o teste, associando a categoria válida
        self.clube = Clube.objects.create(
            moderador=self.user,
            titulo='Clube de Leitura',
            modalidade=None,
            categoria=self.categoria  # Referencia uma categoria válida
        )

        # URL para adicionar o comentário
        self.url = reverse('add_comentario', kwargs={'pk': self.clube.pk})

    def test_usuario_pode_adicionar_comentario(self):
        # Autentica o usuário
        self.client.login(username='testuser', password='12345')

        # Dados do comentário a ser postado
        comentario_data = {
            'comentario': 'Esse é um comentário de teste.'
        }

        # Faz uma requisição POST para adicionar o comentário
        response = self.client.post(self.url, comentario_data)

        # Verifica se o redirecionamento após adicionar o comentário foi bem-sucedido
        self.assertEqual(response.status_code, 302)

        # Verifica se o comentário foi criado
        comentario = Comentario.objects.filter(clube=self.clube, user=self.user).first()
        self.assertIsNotNone(comentario)

        # Verifica se o conteúdo do comentário é o que foi enviado
        self.assertEqual(comentario.comentario, 'Esse é um comentário de teste.')

    def test_usuario_nao_autenticado_nao_pode_comentar(self):
    # Dados do comentário a ser postado
        comentario_data = {
            'comentario': 'Esse é um comentário de teste.'
        }

        # Faz uma requisição POST sem estar logado
        response = self.client.post(self.url, comentario_data)

        # Verifica se o redirecionamento ocorreu para a página de login correta (/login/)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/login/?next={self.url}')  # Atualizando a URL para '/login/'

        # Verifica que nenhum comentário foi criado
        self.assertFalse(Comentario.objects.exists())