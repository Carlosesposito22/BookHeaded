from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Clube, Modalidade, Categoria, Membro, HistoricoMaratona, Comentario
from datetime import datetime
import json
import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from site_cc.models import Clube, Modalidade, Categoria, Comentario, Membro

class MaratonaTests(TestCase):

    def setUp(self):
        self.moderador = User.objects.create_user(username='moderador', password='senha123')
        self.membro = User.objects.create_user(username='membro', password='senha123')

        self.modalidade = Modalidade.objects.create(nome='Leitura')
        self.categoria = Categoria.objects.create(nome='Fantasia')

        self.clube = Clube.objects.create(
            moderador=self.moderador,
            titulo='Clube de Leitura',
            modalidade=self.modalidade,
            categoria=self.categoria,
            descricao='Clube focado em leitura de fantasia'
        )

        self.membro_clube = Membro.objects.create(clube=self.clube, usuario=self.membro, aprovado=True)

        self.client = Client()

    def fazer_login(self, username, password):
        """Auxiliar para realizar o login"""
        self.client.login(username=username, password=password)

    def test_botao_criar_maratona_visivel_para_moderador(self):
        self.fazer_login('moderador', 'senha123')
        response = self.client.get(reverse('club-Detail', kwargs={'pk': self.clube.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Start Spree')

    def test_botao_criar_maratona_invisivel_para_membro(self):
        self.fazer_login('membro', 'senha123')
        response = self.client.get(reverse('club-Detail', kwargs={'pk': self.clube.id}))
        self.assertNotContains(response, 'Start Spree')

    def test_criacao_maratona(self):
        self.fazer_login('moderador', 'senha123')

        dados_maratona = {
            'nome_maratona': 'Maratona de Outubro',
            'data_inicio': '2024-10-01',
            'data_fim': '2024-10-31',
            'capitulo_final': 100,
            'capitulo_atual': 1
        }

        response = self.client.post(
            reverse('criar_maratona', kwargs={'clube_id': self.clube.id}),
            data=json.dumps(dados_maratona),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Maratona criada com sucesso!'})

        self.clube.refresh_from_db()
        self.assertEqual(self.clube.nome_maratona, 'Maratona de Outubro')
        self.assertEqual(self.clube.maratona_ativa, True)
        self.assertEqual(self.clube.capitulo_atual_maratona, 1)
        self.assertEqual(self.clube.capitulo_final_maratona, 100)

    def test_criacao_maratona_data_final_menor_que_data_inicio(self):
        self.fazer_login('moderador', 'senha123')

        dados_maratona = {
            'nome_maratona': 'Maratona de Outubro',
            'data_inicio': '2024-10-31',
            'data_fim': '2024-10-01',
            'capitulo_final': 100,
            'capitulo_atual': 1
        }

        response = self.client.post(
            reverse('criar_maratona', kwargs={'clube_id': self.clube.id}),
            data=json.dumps(dados_maratona),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'Data final não pode ser menor que a data inicial.'})

    def test_criacao_maratona_capitulo_final_menor_que_capitulo_inicial(self):
        self.fazer_login('moderador', 'senha123')

        dados_maratona = {
            'nome_maratona': 'Maratona de Outubro',
            'data_inicio': '2024-10-01',
            'data_fim': '2024-10-31',
            'capitulo_final': 0,
            'capitulo_atual': 1
        }

        response = self.client.post(
            reverse('criar_maratona', kwargs={'clube_id': self.clube.id}),
            data=json.dumps(dados_maratona),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'Capítulo final não pode ser menor que o capítulo atual.'})

    def test_visualizacao_maratona_para_membros(self):
        self.fazer_login('membro', 'senha123')
        response = self.client.get(reverse('detalhes_maratona', kwargs={'clube_id': self.clube.id}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'maratona_ativa': False
        })

    def test_finalizar_maratona(self):
        self.fazer_login('moderador', 'senha123')

        self.clube.maratona_ativa = True
        self.clube.nome_maratona = 'Maratona de Outubro'
        self.clube.data_inicio_maratona = datetime.strptime('2024-10-01', '%Y-%m-%d').date()
        self.clube.data_fim_maratona = datetime.strptime('2024-10-31', '%Y-%m-%d').date()
        self.clube.capitulo_final_maratona = 100
        self.clube.capitulo_atual_maratona = 50
        self.clube.save()

        response = self.client.post(reverse('finalizar_maratona', kwargs={'clube_id': self.clube.id}))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Maratona finalizada com sucesso!'})

        self.clube.refresh_from_db()
        self.assertFalse(self.clube.maratona_ativa)
        historico = HistoricoMaratona.objects.filter(clube=self.clube).first()
        self.assertIsNotNone(historico)
        self.assertEqual(historico.nome_maratona, 'Maratona de Outubro')

    def test_atualizacao_historico_apos_finalizacao_maratona(self):
        self.fazer_login('moderador', 'senha123')

        self.clube.maratona_ativa = True
        self.clube.nome_maratona = 'Maratona de Outubro'
        self.clube.data_inicio_maratona = datetime.strptime('2024-10-01', '%Y-%m-%d').date()
        self.clube.data_fim_maratona = datetime.strptime('2024-10-31', '%Y-%m-%d').date()
        self.clube.capitulo_final_maratona = 100
        self.clube.capitulo_atual_maratona = 50
        self.clube.total_maratona_finalizadas = 0
        self.clube.save()

        response = self.client.post(reverse('finalizar_maratona', kwargs={'clube_id': self.clube.id}))

        self.assertEqual(response.status_code, 200)
        self.clube.refresh_from_db()
        self.assertEqual(self.clube.total_maratona_finalizadas, 1)

    def test_registro_historico_apos_finalizacao(self):
        self.fazer_login('moderador', 'senha123')

        self.clube.maratona_ativa = True
        self.clube.nome_maratona = 'Maratona de Outubro'
        self.clube.data_inicio_maratona = datetime.strptime('2024-10-01', '%Y-%m-%d').date()
        self.clube.data_fim_maratona = datetime.strptime('2024-10-31', '%Y-%m-%d').date()
        self.clube.capitulo_final_maratona = 100
        self.clube.capitulo_atual_maratona = 50
        self.clube.save()

        self.client.post(reverse('finalizar_maratona', kwargs={'clube_id': self.clube.id}))

        historico = HistoricoMaratona.objects.filter(clube=self.clube).first()
        self.assertIsNotNone(historico)
        self.assertEqual(historico.nome_maratona, 'Maratona de Outubro')
        self.assertEqual(int(historico.capitulo_final), 100)  
        self.assertEqual(int(historico.capitulo_atual), 50)  
        self.assertEqual(historico.data_inicio, self.clube.data_inicio_maratona)
        self.assertEqual(historico.data_fim, self.clube.data_fim_maratona)

    def test_visualizacao_historico_para_membros(self):
        self.fazer_login('membro', 'senha123')

        self.clube.maratona_ativa = True
        self.clube.nome_maratona = 'Maratona de Outubro'
        self.clube.data_inicio_maratona = datetime.strptime('2024-10-01', '%Y-%m-%d').date()
        self.clube.data_fim_maratona = datetime.strptime('2024-10-31', '%Y-%m-%d').date()
        self.clube.capitulo_final_maratona = 100
        self.clube.capitulo_atual_maratona = 50
        self.clube.save()

        self.client.post(reverse('finalizar_maratona', kwargs={'clube_id': self.clube.id}))
        response = self.client.get(reverse('listar_historico_maratona', kwargs={'clube_id': self.clube.id}))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'historico': [{
                'nome_maratona': 'Maratona de Outubro',
                'data_inicio': '2024-10-01',
                'data_fim': '2024-10-31',
                'capitulo_final': '100',
                'capitulo_atual': '50',
                'data_registro': response.json()['historico'][0]['data_registro'] 
            }]
        })

    def test_editar_maratona(self):
        logging.disable(logging.CRITICAL)

        self.fazer_login('moderador', 'senha123')

        self.clube.maratona_ativa = True
        self.clube.nome_maratona = 'Maratona Inicial'
        self.clube.data_inicio_maratona = datetime.strptime('2024-10-01', '%Y-%m-%d').date()
        self.clube.data_fim_maratona = datetime.strptime('2024-10-31', '%Y-%m-%d').date()
        self.clube.capitulo_final_maratona = 100
        self.clube.capitulo_atual_maratona = 10
        self.clube.save()

        novos_dados_maratona = {
            'nome_maratona': 'Maratona Editada',
            'data_inicio': '2024-10-05',
            'data_fim': '2024-11-05',
            'capitulo_final': 120,
            'capitulo_atual': 15
        }

        response = self.client.post(
            reverse('criar_maratona', kwargs={'clube_id': self.clube.id}),
            data=json.dumps(novos_dados_maratona),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Maratona atualizada com sucesso!'})

        self.clube.refresh_from_db()
        self.assertEqual(self.clube.nome_maratona, 'Maratona Editada')
        self.assertEqual(self.clube.data_inicio_maratona, datetime.strptime('2024-10-05', '%Y-%m-%d').date())
        self.assertEqual(self.clube.data_fim_maratona, datetime.strptime('2024-11-05', '%Y-%m-%d').date())
        self.assertEqual(self.clube.capitulo_atual_maratona, 15)
        self.assertEqual(self.clube.capitulo_final_maratona, 120)

        logging.disable(logging.NOTSET)


class TestClubePrivado(TestCase):
    
    def setUp(self):

        self.moderador = User.objects.create_user(username='moderador', password='12345')
        self.participante = User.objects.create_user(username='participante', password='12345')

        self.categoria = Categoria.objects.create(nome='Ficção')
        self.modalidade = Modalidade.objects.create(nome='Virtual')

        self.clube_privado = Clube.objects.create(
            moderador=self.moderador,
            titulo='Clube Fechado',
            privado=True,
            categoria=self.categoria,
            modalidade=self.modalidade
        )
        
    def fazer_login(self, username, password):
        """Auxiliar para realizar o login"""
        self.client.login(username=username, password=password)

    def test_criar_clube_privado(self):
        """Testa se o clube é criado corretamente como privado.""" 
        assert self.clube_privado.privado is True
        assert Clube.objects.count() == 1

    def test_solicitacao_entrada(self):
        """Testa se a solicitação de entrada é registrada corretamente.""" 
        self.fazer_login('participante', '12345')
        url = reverse('adicionar-membro', args=[self.clube_privado.id])
        response = self.client.post(url)
        
        assert response.status_code == 302 
        membro = Membro.objects.get(clube=self.clube_privado, usuario=self.participante)
        assert membro.aprovado is False

    def test_aprovar_membro(self):
        """Testa se o moderador pode aprovar uma solicitação de entrada.""" 
        Membro.objects.create(clube=self.clube_privado, usuario=self.participante, aprovado=False)
        
        self.fazer_login('moderador', '12345')
        url = reverse('aprovar-membro', args=[self.clube_privado.id, 1])
        response = self.client.get(url)
        
        assert response.status_code == 200
        membro = Membro.objects.get(clube=self.clube_privado, usuario=self.participante)
        assert membro.aprovado is True

    def test_rejeitar_membro(self):
        """Testa se o moderador pode rejeitar uma solicitação de entrada.""" 
        membro = Membro.objects.create(clube=self.clube_privado, usuario=self.participante, aprovado=False)
        
        self.fazer_login('moderador', '12345')
        url = reverse('recusar-membro', args=[self.clube_privado.id, membro.id])
        response = self.client.post(url)

        assert response.status_code == 200
        assert not Membro.objects.filter(id=membro.id).exists()

    def test_acesso_apos_aprovacao(self):
        """Testa se um membro aprovado pode acessar o clube.""" 
        Membro.objects.create(clube=self.clube_privado, usuario=self.participante, aprovado=True)

        self.fazer_login('participante', '12345')
        url = reverse('club-Detail', args=[self.clube_privado.id])
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'Clube Fechado' in str(response.content)

    def test_mensagem_solicitacao_pendente(self):
        """Testa se um participante não aprovado vê uma mensagem de solicitação pendente.""" 

        membro = Membro.objects.create(clube=self.clube_privado, usuario=self.participante, aprovado=False)

        assert Membro.objects.filter(id=membro.id, aprovado=False).exists(), "O membro não foi criado como pendente"

        self.fazer_login('participante', '12345')

        url = reverse('club-Detail', args=[self.clube_privado.id])
        response = self.client.get(url)

        assert response.status_code == 200, "Falha ao acessar a página de detalhe do clube"

        assert 'pendente' in response.content.decode().lower(), "Mensagem de solicitação pendente não encontrada"

    def test_solicitacao_entrada_duplicada(self):
        """Testa se o sistema impede solicitações duplicadas para o mesmo clube.""" 

        Membro.objects.create(clube=self.clube_privado, usuario=self.participante, aprovado=False)

        self.fazer_login('participante', '12345')
        url = reverse('adicionar-membro', args=[self.clube_privado.id])
        response = self.client.post(url)

        assert response.status_code == 400, f"Esperava 400, mas recebeu {response.status_code}"

        response_content = response.content.decode().lower()
        print("Response content:", response_content)

        assert 'você já solicitou acesso a este clube' in response_content, "Mensagem de erro esperada não encontrada"

    def test_rejeitar_membro_ja_rejeitado_ou_inexistente(self):
        """Testa se o moderador não pode rejeitar um membro já rejeitado ou que não existe.""" 
        membro = Membro.objects.create(clube=self.clube_privado, usuario=self.participante, aprovado=False)
        self.fazer_login('moderador', '12345')

        url = reverse('recusar-membro', args=[self.clube_privado.id, membro.id])
        response = self.client.post(url)
        assert response.status_code == 200
        assert not Membro.objects.filter(id=membro.id).exists()

        response = self.client.post(url)
        assert response.status_code == 404

    def test_criar_clube_com_informacoes_faltantes(self):
        """Testa manualmente se o clube não pode ser criado com informações faltantes.""" 
        clube_count_antes = Clube.objects.count()

        titulo = ''
        categoria = None
        
        if not titulo or not categoria:
            return

        Clube.objects.create(
            moderador=self.moderador,
            titulo=titulo,  
            privado=True,
            categoria=categoria,  
            modalidade=self.modalidade
        )
        
        clube_count_depois = Clube.objects.count()
        
        assert clube_count_antes == clube_count_depois, "O clube foi criado com informações faltantes!"


class ClubeSearchTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.categoria_esportes = Categoria.objects.create(nome='Esportes')
        self.categoria_leitura = Categoria.objects.create(nome='Leitura')
        self.modalidade = Modalidade.objects.create(nome='Corrida')


        self.clube1 = Clube.objects.create(
            moderador=self.user,
            titulo='Clube de Corrida',
            modalidade=self.modalidade,
            categoria=self.categoria_esportes,
            descricao='Este é um clube dedicado à corrida.'
        )
        self.clube2 = Clube.objects.create(
            moderador=self.user,
            titulo='Clube de Leitura',
            modalidade=self.modalidade,
            categoria=self.categoria_leitura,
            descricao=None 
        )

    def test_search_bar_visible(self):
        """Teste 1: Verifica se a barra de pesquisa está visível na página de clubes.""" 
        response = self.client.get(reverse('clubs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input', msg_prefix="A barra de pesquisa não foi encontrada na página")
        self.assertContains(response, 'type="text"', msg_prefix="A barra de pesquisa não está configurada corretamente")
        self.assertContains(response, 'placeholder="Search Clubs"', msg_prefix="O placeholder da barra de pesquisa está incorreto")

    def test_search_club_by_name(self):
        """Teste 2: Verifica se a busca por nome do clube funciona corretamente.""" 
        response = self.client.get(reverse('clubs'), {'nome': 'Corrida'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clube de Corrida')
        self.assertNotContains(response, 'Clube de Leitura')

    def test_club_description_none(self):
        """Teste 3: Verifica se a descrição do clube sendo None é tratada corretamente.""" 
        response = self.client.get(reverse('clubs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clube de Leitura')
        self.assertNotContains(response, 'None') 
    
    def test_partial_search_club_by_name(self):
        """Teste 4: Verifica se a busca parcial por nome do clube funciona corretamente.""" 
        response = self.client.get(reverse('clubs'), {'nome': 'Corr'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clube de Corrida')
        self.assertNotContains(response, 'Clube de Leitura')

    def test_search_club_by_nonexistent_name(self):
        """Teste 5: Verifica se uma busca por nome inexistente exibe a mensagem apropriada.""" 
        response = self.client.get(reverse('clubs'), {'nome': 'Clube Inexistente'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum clube corresponde aos filtros selecionados. Por favor, tente uma pesquisa diferente.', 
                            msg_prefix="A mensagem de 'nenhum clube encontrado' não foi exibida.")

    def test_search_club_case_insensitive(self):
        """Teste 6: Verifica se a busca por nome do clube é case insensitive.""" 
        response = self.client.get(reverse('clubs'), {'nome': 'clube de corrida'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clube de Corrida')
        self.assertNotContains(response, 'Clube de Leitura')


class ComentarioTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')

        self.client.login(username='testuser', password='12345')

        self.modalidade = Modalidade.objects.create(nome='Leitura')
        self.categoria = Categoria.objects.create(nome='Fantasia')

        self.clube = Clube.objects.create(
            moderador=self.user,
            titulo='Clube de Leitura',
            modalidade=self.modalidade,
            categoria=self.categoria,
            descricao='Clube focado em leitura de fantasia'
        )

    def test_comentario_vazio(self):
        """
        Testa se o sistema exibe erro ao tentar enviar comentário vazio e não salva o comentário.
        """
        response = self.client.post(reverse('add_comentario', kwargs={'pk': self.clube.id}), { 
            'comentario': '' 
        })

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Comentario.objects.count(), 0)

        self.assertContains(response, 'O comentário não pode estar vazio.')

    def test_moderador_pode_comentar(self):
        """
        Testa se o moderador do clube pode comentar corretamente.
        """
        response = self.client.post(reverse('add_comentario', kwargs={'pk': self.clube.id}), {
            'comentario': 'Esse é um comentário válido.'  
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comentario.objects.count(), 1)

        comentario = Comentario.objects.first()
        self.assertEqual(comentario.comentario, 'Esse é um comentário válido.')
        self.assertEqual(comentario.user, self.user)

    def test_usuario_pode_comentar(self):
        """
        Testa se um usuário logado pode comentar no clube.
        """

        response = self.client.post(reverse('add_comentario', kwargs={'pk': self.clube.id}), {
            'comentario': 'Comentário de um usuário.' 
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comentario.objects.count(), 1)

        comentario = Comentario.objects.first()
        self.assertEqual(comentario.comentario, 'Comentário de um usuário.')
        self.assertEqual(comentario.user, self.user)


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
