from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Clube, Membro, Categoria, Modalidade

class SairDoClubeTest(TestCase):

    def setUp(self):
        # Recuperar categoria e modalidade já existentes, criadas pelo signals.py
        self.categoria = Categoria.objects.get(nome='Ficção')
        self.modalidade = Modalidade.objects.get(nome='Online')

        # Criar um usuário e logá-lo como moderador
        self.moderador = User.objects.create_user(username='moderador', password='Asd12345678')
        self.client.login(username='moderador', password='Asd12345678')

        # Criar um clube com categoria e modalidade, e adicionar o moderador como moderador
        self.clube = Clube.objects.create(
            titulo='Clube de Teste',
            moderador=self.moderador,
            descricao='Um clube de teste',
            categoria=self.categoria,
            modalidade=self.modalidade
        )

        # Criar outro usuário que será um membro comum
        self.membro = User.objects.create_user(username='membro', password='Asd12345678')
        Membro.objects.create(clube=self.clube, usuario=self.membro)

    def test_botao_nao_aparece_para_moderador(self):
        # Acessar a página do clube como moderador (onde o botão de sair NÃO deveria estar)
        response = self.client.get(reverse('club-Detail', args=[self.clube.id]))
        
        # Verificar que o botão "Sair do Clube" NÃO está presente no HTML para o moderador
        self.assertNotContains(response, '<button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#sairDoClubeModal-{{ clube.id }}">Sair do Clube</button>')

    def test_botao_sair_do_clube_aparece_para_membro(self):
        # Logar como membro
        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        # Acessar a página do clube (onde o botão de sair deveria estar para o membro)
        response = self.client.get(reverse('club-Detail', args=[self.clube.id]))
        
        # Verificar se o botão "Sair do Clube" está presente no HTML para o membro
        self.assertContains(response, 'Sair do Clube')

    def test_usuario_sai_do_clube(self):
        # Logar como membro
        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        # Testa se o usuário é removido corretamente da lista de membros
        response = self.client.post(reverse('sair-do-clube', args=[self.clube.id]))
        
        # Verificar se o membro foi removido
        self.assertFalse(Membro.objects.filter(clube=self.clube, usuario=self.membro).exists())

        # Verificar se a mensagem de sucesso foi enviada
        self.assertRedirects(response, reverse('myclubes'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Você saiu do clube "{self.clube.titulo}"')


class FavoritarClubeTest(TestCase):

    def setUp(self):
        # Recuperar categoria e modalidade já existentes, criadas pelo signals.py
        self.categoria = Categoria.objects.get(nome='Ficção')
        self.modalidade = Modalidade.objects.get(nome='Online')

        # Criar um usuário moderador e logá-lo
        self.moderador = User.objects.create_user(username='moderador', password='Asd12345678')
        self.client.login(username='moderador', password='Asd12345678')

        # Criar um clube e adicionar o moderador como moderador do clube
        self.clube = Clube.objects.create(
            titulo='Clube de Teste',
            moderador=self.moderador,
            descricao='Clube para testes de funcionalidade',
            categoria=self.categoria,
            modalidade=self.modalidade
        )

        # Criar um usuário membro
        self.membro = User.objects.create_user(username='membro', password='Asd12345678')

    def test_usuario_logado_pode_favoritar_clube(self):
        # Logar como membro
        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        # Favoritar o clube
        response = self.client.post(reverse('favoritar_clube', args=[self.clube.id]))

        # Verificar se o clube foi favoritado corretamente
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.membro in self.clube.favoritos.all())

    def test_lista_de_clubes_favoritos_atualizada(self):
        # Logar como membro
        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        # Favoritar o clube
        self.client.post(reverse('favoritar_clube', args=[self.clube.id]))

        # Verificar se o clube está na lista de favoritos do usuário
        self.assertTrue(self.clube in self.membro.clubes_favoritos.all())

    def test_usuario_pode_visualizar_clubes_favoritos(self):
        # Logar como membro
        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        # Adicionar o clube aos favoritos do membro
        self.membro.clubes_favoritos.add(self.clube)

        # Acessar a página onde os favoritos são exibidos (ajustar a URL correta para 'myclubes')
        response = self.client.get(reverse('myclubes'))

        # Verificar se o título do clube favoritado aparece na lista de favoritos
        self.assertContains(response, self.clube.titulo)

        # Verificar se o ícone de estrela preenchida aparece indicando que o clube está favoritado
        self.assertContains(response, '<i class="bi bi-star-fill star-from-btn"></i>')

    def test_usuario_pode_desfavoritar_clube(self):
        # Logar como membro
        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        # Favoritar o clube e depois desfavoritar
        self.client.post(reverse('favoritar_clube', args=[self.clube.id]))
        response = self.client.post(reverse('favoritar_clube', args=[self.clube.id]))

        # Verificar se o clube foi removido dos favoritos
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.membro in self.clube.favoritos.all())


class LivrosFavoritosTest(TestCase):

    def setUp(self):
        # Recuperar categoria e modalidade já existentes, criadas pelo signals.py
        self.categoria = Categoria.objects.get(nome='Ficção')
        self.modalidade = Modalidade.objects.get(nome='Online')

        # Criar um moderador e logá-lo
        self.moderador = User.objects.create_user(username='moderador', password='Asd12345678')
        self.client.login(username='moderador', password='Asd12345678')

        # Criar um clube e associar o moderador ao clube
        self.clube = Clube.objects.create(
            titulo='Clube de Leitura',
            moderador=self.moderador,
            descricao='Clube para leitura de ficção científica',
            categoria=self.categoria,
            modalidade=self.modalidade
        )

        # Criar um membro comum
        self.membro = User.objects.create_user(username='membro', password='Asd12345678')

    def test_moderador_pode_adicionar_livros_favoritos(self):
        # Logar como moderador (já está logado no setup)
        response = self.client.post(reverse('add_top_livros', args=[self.clube.id]), {
            'top_livros': 'Livro 1\nLivro 2\nLivro 3'
        })

        # Verificar se os livros foram adicionados corretamente
        self.clube.refresh_from_db()
        self.assertEqual(self.clube.top_livros, 'Livro 1\nLivro 2\nLivro 3')
        self.assertEqual(response.status_code, 302)  # Redireciona após o sucesso

    def test_membros_podem_visualizar_livros_favoritos(self):
        # Logar como membro
        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        # Adicionar livros pelo moderador
        self.clube.top_livros = 'Livro 1\nLivro 2\nLivro 3'
        self.clube.save()

        # Verificar se os membros conseguem ver a lista de livros favoritos
        response = self.client.get(reverse('club-Detail', args=[self.clube.id]))

        # Verificar se os livros estão sendo exibidos corretamente
        self.assertContains(response, 'Livro 1')
        self.assertContains(response, 'Livro 2')
        self.assertContains(response, 'Livro 3')

    def test_moderador_pode_editar_livros_favoritos(self):
        # Logar como moderador (já está logado no setup)
        self.clube.top_livros = 'Livro 1\nLivro 2'
        self.clube.save()

        # Editar a lista de livros
        response = self.client.post(reverse('add_top_livros', args=[self.clube.id]), {
            'top_livros': 'Livro 1\nLivro 2\nLivro 3'
        })

        # Verificar se a lista foi atualizada corretamente
        self.clube.refresh_from_db()
        self.assertEqual(self.clube.top_livros, 'Livro 1\nLivro 2\nLivro 3')

    def test_membro_nao_pode_editar_livros_favoritos(self):
        # Logar como membro
        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        # Tentar editar a lista de livros favoritos
        response = self.client.post(reverse('add_top_livros', args=[self.clube.id]), {
            'top_livros': 'Livro Indevido'
        })

        # Verificar se a alteração foi negada
        self.assertEqual(response.status_code, 403)
        self.clube.refresh_from_db()
        self.assertNotEqual(self.clube.top_livros, 'Livro Indevido')
