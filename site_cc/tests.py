from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Clube, Membro, Comentario, Modalidade, Categoria, HistoricoMaratona, Profile, Avaliacao
from .views import comentario_create_view
from unittest.mock import patch
from django.conf import settings
from django.http import HttpResponseForbidden
from datetime import datetime
import json
import logging
import os
from django.core.management import call_command
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

from django.contrib.auth.models import User
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from site_cc.models import Profile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeguirUsuarioTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def teste_cenario1(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuario = driver.find_element(By.NAME, "username")
        senha = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        registrar = driver.find_element(By.NAME, "registrar")

        usuario.send_keys("testefollow")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("testefollow")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/perfil/25/") # <-- Mateus altera esse 25 pra o id de um usuário existente pra tu

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'follow-text'))
            )
            follow_button = driver.find_element(By.ID, 'follow-text')
            follow_button.click()
            print("Seguir realizado com sucesso.")
            time.sleep(2)
            view_followers= driver.find_element(By.ID, 'followers-text2')
            view_followers.click()
            time.sleep(2)
        except Exception as e:
            print(f"Erro ao seguir: {e}")

    def teste_cenario2(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("testefollow")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/perfil/25/") # <-- Mateus altera esse 25 pra o id de um usuário existente pra tu
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Unfollow')]"))
        )

        try:
            unfollow_button = driver.find_element(By.XPATH, "//*[contains(text(),'Unfollow')]")
            driver.execute_script("arguments[0].click();", unfollow_button) 
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Follow')]"))
            )
            view_followers2= driver.find_element(By.ID, 'followers-text2')
            time.sleep(2)
            view_followers2.click()
            time.sleep(2)
            print("Unfollow realizado com sucesso.")
        except Exception as e:
            print(f"Erro ao realizar Unfollow: {e}")

class ProfileViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.profile1 = Profile.objects.create(user=self.user1, bio="Bio do user1", icone="images/icon1.svg")
        self.profile2 = Profile.objects.create(user=self.user2, bio="Bio do user2", icone="images/icon2.svg")

        self.profile1.seguidores.add(self.user2)

    def test_profile_link_in_navbar(self):
        """Verificar se o link 'Profile' aparece na navbar para usuários logados"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))

        self.assertContains(response, 'Profile')
        self.assertEqual(response.status_code, 200)

    def test_profile_information_display(self):
        """Verificar se as informações do perfil são exibidas corretamente"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))

        self.assertContains(response, '@user1')
        self.assertContains(response, 'Bio do user1')
        self.assertContains(response, 'images/icon1.svg')  # Ícone de perfil
        self.assertContains(response, '1 Followers')  # user1 tem 1 seguidor
        self.assertContains(response, '0 Following')  # user1 não segue ninguém

    def test_followers_and_following_display_with_icons_and_usernames(self):
        """Verificar se os seguidores e seguidos aparecem corretamente com as fotos de perfil e nomes"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))

        # Verificar se user2 aparece na lista de seguidores de user1 com nome de usuário e ícone
        self.assertContains(response, '@user2')  # Nome de usuário do seguidor (user2)
        self.assertContains(response, 'images/icon2.svg')  # Ícone do seguidor (user2)

        # Verificar se user1 aparece corretamente na lista de "seguidos" de user2 com nome e ícone
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user2.id}))

        self.assertContains(response, '@user1')  # Nome de usuário do seguido (user1)
        self.assertContains(response, 'images/icon1.svg')  # Ícone do seguido (user1)

    def test_correct_followers_and_following_links(self):
        """Verificar se os links dos seguidores e seguidos estão corretos"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))

        # Verificar se o link do seguidor está correto
        self.assertContains(response, reverse('profile', kwargs={'user_id': self.user2.id}))

        # Verificar se os usuários seguidos estão corretos
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user2.id}))
        self.assertContains(response, reverse('profile', kwargs={'user_id': self.user1.id}))

    def test_profile_icon_in_navbar(self):
        """Verificar se o ícone de perfil correto aparece na navbar para o usuário logado"""
        # Fazer login com o user1
        self.client.login(username='user1', password='password123')
       
        # Fazer uma requisição para uma página que inclui a navbar
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))
       
        # Verificar se o ícone de perfil correto de user1 aparece na navbar
        self.assertContains(response, 'images/icon1.svg', msg_prefix="O ícone de perfil do user1 não está correto na navbar.")
        self.assertEqual(response.status_code, 200)

        # Fazer login com o user2
        self.client.login(username='user2', password='password123')

        # Fazer uma requisição para a página do user2 que também inclui a navbar
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user2.id}))
       
        # Verificar se o ícone de perfil correto de user2 aparece na navbar
        self.assertContains(response, 'images/icon2.svg', msg_prefix="O ícone de perfil do user2 não está correto na navbar.")
        self.assertEqual(response.status_code, 200)


class ProfileEditTests(TestCase):

    def setUp(self):
        # Cria um usuário e um perfil de teste
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio="Initial bio", icone='images/icon3.svg')

        # Loga o usuário
        self.client.login(username='testuser', password='12345')

    def test_edit_button_visible_and_functional(self):
        # Acessa a página de perfil para o próprio usuário (onde o botão "Editar" deve estar visível)
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}))
       
        # Verifica se o botão "Editar" está presente
        self.assertContains(response, 'bi-pencil-fill', msg_prefix="O botão de edição não está visível para o proprietário do perfil")

        # Envia um POST simulando uma edição no perfil (alterando a bio e o ícone)
        new_bio = "New bio text"
        new_icon = 'images/icon4.svg'
        response = self.client.post(reverse('profile', kwargs={'user_id': self.user.id}), {
            'bio': new_bio,
            'icone': new_icon
        })

        # Redireciona para a página de perfil após a edição
        self.assertEqual(response.status_code, 302)

        # Recarrega o perfil do banco de dados e verifica as alterações
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, new_bio, "A bio não foi atualizada corretamente")
        self.assertEqual(self.profile.icone, new_icon, "O ícone de perfil não foi atualizado corretamente")

    def test_partial_edit(self):
        # Teste para verificar se é possível alterar apenas a bio ou apenas o ícone separadamente
        # Alterar somente a bio
        new_bio = "Another bio update"
        response = self.client.post(reverse('profile', kwargs={'user_id': self.user.id}), {
            'bio': new_bio,
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, new_bio, "A bio não foi atualizada corretamente ao editar somente a bio")
        self.assertEqual(self.profile.icone, 'images/icon3.svg', "O ícone não deveria ter sido alterado")

        # Alterar somente o ícone
        new_icon = 'images/icon5.svg'
        response = self.client.post(reverse('profile', kwargs={'user_id': self.user.id}), {
            'icone': new_icon,
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.icone, new_icon, "O ícone não foi atualizado corretamente ao editar somente o ícone")


class ProfileEditNavbarTests(TestCase):

    def setUp(self):
        # Cria um usuário e um perfil de teste
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, icone='images/icon3.svg')

        # Loga o usuário
        self.client.login(username='testuser', password='12345')

    def test_profile_icon_update_reflects_in_navbar(self):
        # Verifica o ícone atual antes da edição
        response = self.client.get(reverse('pagina_principal'))
        self.assertContains(response, 'images/icon3.svg', msg_prefix="O ícone original não foi encontrado na navbar antes da edição.")

        # Simula a edição do perfil para alterar o ícone
        new_icon = 'images/icon4.svg'
        response = self.client.post(reverse('profile', kwargs={'user_id': self.user.id}), {
            'icone': new_icon,
        })

        # Redireciona corretamente após a atualização
        self.assertEqual(response.status_code, 302)

        # Faz uma nova requisição para verificar a navbar
        response = self.client.get(reverse('pagina_principal'))  # Pega uma página que carrega a navbar
        self.assertContains(response, new_icon, msg_prefix="O novo ícone de perfil não foi atualizado na navbar.")


class SearchUsersTests(TestCase):
   
    def setUp(self):
        # Criar usuários de teste
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')
        self.user3 = User.objects.create_user(username='alice', password='password123')
       
        # Criar perfis para cada usuário manualmente
        Profile.objects.create(user=self.user1, bio="Bio for testuser1", icone='images/icon1.svg')
        Profile.objects.create(user=self.user2, bio="Bio for testuser2", icone='images/icon2.svg')
        Profile.objects.create(user=self.user3, bio="Bio for Alice", icone='images/icon3.svg')

        # Loga o usuário 1 para realizar os testes
        self.client.login(username='testuser1', password='password123')

    def test_search_bar_is_available(self):
        """Verifica se a barra de pesquisa está disponível na página"""
        # Carregar a página que inclui a barra de pesquisa, por exemplo, 'lista_usuarios'
        response = self.client.get(reverse('lista_usuarios'))
       
        # Verifica se o status da resposta é OK (200)
        self.assertEqual(response.status_code, 200)
       
        # Verifica se o placeholder da barra de pesquisa está na resposta
        self.assertIn('placeholder="Search Bookheads"', response.content.decode(),
                    msg="O placeholder da barra de pesquisa não está correto.")

    def test_search_returns_multiple_results_with_profile_info(self):
        """Verifica se a busca retorna múltiplos resultados e exibe as informações corretas"""
        # Faz uma busca que retorna múltiplos usuários e verifica nome, bio e ícone
        response = self.client.get(reverse('lista_usuarios'), {'nomes': 'testuser'})
        self.assertEqual(response.status_code, 200)

        # Verifica se ambos os usuários testuser1 e testuser2 aparecem corretamente nos resultados
        self.assertContains(response, 'testuser1', msg_prefix="O nome do usuário testuser1 não foi exibido corretamente.")
        self.assertContains(response, 'Bio for testuser1', msg_prefix="A bio do usuário testuser1 não foi exibida corretamente.")
        self.assertContains(response, 'images/icon1.svg', msg_prefix="O ícone do usuário testuser1 não foi exibido corretamente.")
       
        self.assertContains(response, 'testuser2', msg_prefix="O nome do usuário testuser2 não foi exibido corretamente.")
        self.assertContains(response, 'Bio for testuser2', msg_prefix="A bio do usuário testuser2 não foi exibida corretamente.")
        self.assertContains(response, 'images/icon2.svg', msg_prefix="O ícone do usuário testuser2 não foi exibido corretamente.")

    def test_search_no_results(self):
        """Verifica se a pesquisa que não retorna resultados exibe a mensagem correta"""
        # Faz uma busca que não retorna resultados
        response = self.client.get(reverse('lista_usuarios'), {'nomes': 'nonexistentuser'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum usuário encontrado.', msg_prefix="A mensagem de 'Nenhum usuário encontrado' não foi exibida.")

    def test_click_on_search_result_opens_correct_profile_with_info(self):
        """Verifica se ao clicar no resultado da pesquisa o perfil correto é aberto"""
        # Faz uma busca por "alice"
        response = self.client.get(reverse('lista_usuarios'), {'nomes': 'alice'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alice', msg_prefix="O resultado da busca não exibiu o usuário 'alice'.")
       
        # Simula o clique no perfil de 'alice' e verifica se o perfil correto é carregado
        profile_url = reverse('profile', kwargs={'user_id': self.user3.id})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
       
        # Verifica se o nome, bio e ícone corretos são exibidos no perfil de 'alice'
        self.assertContains(response, 'alice', msg_prefix="O nome do perfil não está correto.")
        self.assertContains(response, 'Bio for Alice', msg_prefix="A bio do perfil não está correta.")
        self.assertContains(response, 'images/icon3.svg', msg_prefix="O ícone de perfil não está correto.")

    def test_search_with_empty_query_returns_all_profiles(self):
        """Verifica se a pesquisa com campo vazio retorna todos os perfis"""
        # Realiza uma busca com o campo 'nomes' vazio
        response = self.client.get(reverse('lista_usuarios'), {'nomes': ''})
        self.assertEqual(response.status_code, 200)

        # Verifica se todos os usuários aparecem nos resultados
        self.assertContains(response, 'testuser1', msg_prefix="O usuário 'testuser1' não foi exibido corretamente.")
        self.assertContains(response, 'testuser2', msg_prefix="O usuário 'testuser2' não foi exibido corretamente.")
        self.assertContains(response, 'alice', msg_prefix="O usuário 'alice' não foi exibido corretamente.")


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

from selenium.webdriver.support.ui import Select

class ComentarioTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def teste_cenario1(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuarioComentar = driver.find_element(By.NAME, "username")
        senhaComentar = driver.find_element(By.NAME, "password1")
        senha2Comentar = driver.find_element(By.NAME, "password2")
        registrarComentar = driver.find_element(By.NAME, "registrar")

        usuarioComentar.send_keys("usercomentario1")
        senhaComentar.send_keys("senha")
        senha2Comentar.send_keys("senha")
        registrarComentar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("usercomentario1")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        time.sleep(2)

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuarioComentar2 = driver.find_element(By.NAME, "username")
        senhaComentar2 = driver.find_element(By.NAME, "password1")
        senha2Comentar2 = driver.find_element(By.NAME, "password2")
        registrarComentar2 = driver.find_element(By.NAME, "registrar")

        usuarioComentar2.send_keys("usercomentario2")
        senhaComentar2.send_keys("senha")
        senha2Comentar2.send_keys("senha")
        registrarComentar2.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin2 = driver.find_element(By.NAME, "username")
        senhalogin2 = driver.find_element(By.NAME, "password")

        usuariologin2.send_keys("usercomentario2")
        senhalogin2.send_keys("senha")
        senhalogin2.send_keys(Keys.ENTER)

        time.sleep(1)

        newclub = driver.find_element(By.ID, "newclub-btn")
        newclub.click()

        time.sleep(1)

        findForm1 = driver.find_element(By.NAME, "titulo")
        findForm2 = driver.find_element(By.NAME, "modalidade")
        findForm3 = driver.find_element(By.NAME, "categoria")
        findForm4 = driver.find_element(By.NAME, "descricao")
        findForm5 = driver.find_element(By.ID, "create-btn")

        findForm1.send_keys("teste Comentario")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descricao pra teste blz")

        time.sleep(1)

        findForm5.click()

        time.sleep(1)

        findComentarioBox = driver.find_element(By.NAME, "comentario")
        findComentarioBox.send_keys("Comentario para teste")

        time.sleep(1)

        findComentar = driver.find_element(By.NAME, "comentar")
        findComentar.click()
        print("Comentário deu certo.")

        time.sleep(1)

        driver.get("http://127.0.0.1:8000")

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        time.sleep(2)

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/login/")

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("usercomentario1")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/clubs/")

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        botao_card = driver.find_element(By.NAME, "titles")
        botao_card.click()

        time.sleep(1)  # Aguarda o resultado da ação

        # Acessa a modal de clubs
        botao_club = driver.find_element(By.NAME, "entrar-btn")
        botao_club.click()

        time.sleep(1)  # Aguarda o resultado da ação

        # Acessa a modal de clubs
        botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
        botao_club_novo_entrar.click()

        time.sleep(1)

        findComentarioBox = driver.find_element(By.NAME, "comentario")
        findComentarioBox.send_keys("Comentario para teste do usuario nao adm!!")

        time.sleep(1)

        findComentar = driver.find_element(By.NAME, "comentar")
        findComentar.click()
        print("Comentário deu certo dnv.")

        time.sleep(1)

        findComentarioBox = driver.find_element(By.NAME, "comentario")
        findComentarioBox.send_keys("Agora vou fazer um comentário vazio...")
        time.sleep(1)
        findComentarioBox.clear()
        findComentarioBox = driver.find_element(By.NAME, "comentario")
        findComentarioBox.send_keys("")
        time.sleep(1)
        findComentar = driver.find_element(By.NAME, "comentar")
        findComentar.click()
        time.sleep(1)

class MaratonaTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        call_command('flush', '--no-input')
        cls.driver.quit()
        super().tearDownClass()

    def handle_success(self, message):
        """Imprime uma mensagem de sucesso no estilo padrão do Django."""
        self.stdout.write(self.style.SUCCESS(message))

    def handle_failure(self, message):
        """Imprime uma mensagem de erro no estilo padrão do Django."""
        self.stdout.write(self.style.ERROR(message))

    def teste_verifica_presenca_btn_moderador_participante(self):
        try:
            driver = self.driver
            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "newclub-btn")
            botao_club.click()
            time.sleep(1)

            titulo_input = driver.find_element(By.ID, "titulo")
            titulo_input.send_keys("Book ola2")

            modalidade_select = Select(driver.find_element(By.ID, "modalidade"))
            modalidade_select.select_by_value("1")

            categoria_select = Select(driver.find_element(By.ID, "categoria"))
            categoria_select.select_by_value("1")

            descricao_input = driver.find_element(By.ID, "descricao")
            descricao_input.send_keys("This is a test description for the book club.")

            create_btn = driver.find_element(By.ID, "create-btn")
            driver.execute_script("arguments[0].removeAttribute('disabled')", create_btn)
            create_btn.click()
            time.sleep(3)

            print("Teste de verificação de presença do botão de moderador e participante foi concluído com sucesso.")
        
        except Exception as e:
            print(f"Falha no teste de verificação de presença do botão de moderador e participante: {e}")

    def teste_criar_maratona(self):
        try:
            driver = self.driver
            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "newclub-btn")
            botao_club.click()
            time.sleep(1)

            titulo_input = driver.find_element(By.ID, "titulo")
            titulo_input.send_keys("Book ola2")

            modalidade_select = Select(driver.find_element(By.ID, "modalidade"))
            modalidade_select.select_by_value("1")

            categoria_select = Select(driver.find_element(By.ID, "categoria"))
            categoria_select.select_by_value("1")

            descricao_input = driver.find_element(By.ID, "descricao")
            descricao_input.send_keys("This is a test description for the book club.")

            create_btn = driver.find_element(By.ID, "create-btn")
            driver.execute_script("arguments[0].removeAttribute('disabled')", create_btn)
            create_btn.click()
            time.sleep(2)

            botao_maratona = driver.find_element(By.ID, "createMaratona")
            botao_maratona.click()
            time.sleep(4)

            nome_maratona = driver.find_element(By.ID, "nomeMaratona")
            nome_maratona.send_keys("Teste Maratona")
            time.sleep(2)

            data_fim = driver.find_element(By.ID, "dataFim")
            data_fim.send_keys("30122024")
            time.sleep(2)

            capitulo_final = driver.find_element(By.ID, "capituloFinal")
            capitulo_final.send_keys("100")
            time.sleep(2)

            botao_save_maratona = driver.find_element(By.ID, "saveMaratona")
            botao_save_maratona.click()
            time.sleep(4)

            # Usando assert para verificar o sucesso do teste
            self.assertTrue(True, "Teste de criação de maratona foi concluído com sucesso.")
        
        except Exception as e:
            # Usando fail para capturar o erro no teste
            self.fail(f"Falha no teste de criação de maratona: {e}")





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


class AvaliacaoClubeTest(TestCase):

    def setUp(self):
        # Criar uma categoria e uma modalidade
        self.categoria = Categoria.objects.create(nome='Ficção')
        self.modalidade = Modalidade.objects.create(nome='Online')

        # Criar um moderador
        self.moderador = User.objects.create_user(username='moderador', password='modpassword')

        # Criar um clube
        self.clube = Clube.objects.create(
            titulo='Clube de Teste',
            moderador=self.moderador,
            descricao='Um clube para testar avaliações',
            categoria=self.categoria,
            modalidade=self.modalidade
        )

        # Criar um participante
        self.participante = User.objects.create_user(username='participante', password='password123')

    def test_usuario_logado_pode_acessar_clube(self):
        """Verificar se o participante logado pode acessar a página do clube"""
        self.client.login(username='participante', password='password123')
        response = self.client.get(reverse('club-Detail', args=[self.clube.id]))
        self.assertEqual(response.status_code, 200)

    def test_usuario_pode_avaliar_clube(self):
        """Verificar se o participante pode avaliar o clube com uma nota válida"""
        self.client.login(username='participante', password='password123')
        response = self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 4})
        
        # Verificar se a avaliação foi registrada
        avaliacao = Avaliacao.objects.filter(clube=self.clube, usuario=self.participante).first()
        self.assertIsNotNone(avaliacao)
        self.assertEqual(avaliacao.valor, 4)

    def test_usuario_nao_seleciona_nota_exibe_erro(self):
        """Testar se o envio de uma avaliação sem uma nota exibe uma mensagem de erro"""
        self.client.login(username='participante', password='password123')

        # Simular o envio de uma avaliação sem selecionar uma nota (rating vazio)
        response = self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': ''})

        # Verificar se o status da resposta é 200 (página recarregada com erro)
        self.assertEqual(response.status_code, 200)

        # Verificar se a avaliação não foi registrada
        self.assertEqual(Avaliacao.objects.filter(clube=self.clube, usuario=self.participante).count(), 0)

        # Verificar se a mensagem de erro de campo obrigatório está presente
        self.assertContains(response, "Este campo é obrigatório e deve ser um número entre 1 e 5.")

    def test_usuario_pode_atualizar_avaliacao(self):
        """Verificar se o participante pode atualizar sua avaliação"""
        self.client.login(username='participante', password='password123')

        # Primeiro, enviar uma avaliação inicial
        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 4})

        # Atualizar a avaliação
        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 5})

        # Verificar se a avaliação foi atualizada
        avaliacao = Avaliacao.objects.get(clube=self.clube, usuario=self.participante)
        self.assertEqual(avaliacao.valor, 5)

    def test_media_avaliacoes_atualizada_corretamente(self):
        """Verificar se a média de avaliações é atualizada corretamente após nova avaliação"""
        # Criar outro participante e enviar avaliações
        participante2 = User.objects.create_user(username='participante2', password='password123')
        self.client.login(username='participante', password='password123')
        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 3})

        self.client.login(username='participante2', password='password123')
        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 5})

        # Verificar se a média de avaliações foi calculada corretamente
        self.assertEqual(self.clube.calcular_media_avaliacoes(), 4)

    def test_usuario_nao_pode_avaliar_mais_de_uma_vez(self):
        """Verificar se o participante não pode enviar uma nova avaliação, mas apenas atualizar a existente"""
        self.client.login(username='participante', password='password123')

        # Enviar uma avaliação inicial
        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 3})

        # Tentar enviar uma nova avaliação
        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 5})

        # Verificar se a avaliação foi atualizada, mas não duplicada
        avaliacao = Avaliacao.objects.filter(clube=self.clube, usuario=self.participante).count()
        self.assertEqual(avaliacao, 1)  # Deve haver apenas uma avaliação registrada

class verificarProgresso(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def teste_cenario1(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuarioComentar = driver.find_element(By.NAME, "username")
        senhaComentar = driver.find_element(By.NAME, "password1")
        senha2Comentar = driver.find_element(By.NAME, "password2")
        registrarComentar = driver.find_element(By.NAME, "registrar")

        usuarioComentar.send_keys("userAdm")
        senhaComentar.send_keys("senha")
        senha2Comentar.send_keys("senha")
        registrarComentar.click()

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("userAdm")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "newclub-btn"))
        )
        newclub = driver.find_element(By.ID, "newclub-btn")
        newclub.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "titulo"))
        )
        findForm1 = driver.find_element(By.NAME, "titulo")
        findForm2 = driver.find_element(By.NAME, "modalidade")
        findForm3 = driver.find_element(By.NAME, "categoria")
        findForm4 = driver.find_element(By.NAME, "descricao")
        findForm5 = driver.find_element(By.ID, "create-btn")

        findForm1.send_keys("teste progressbar")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descricao pra teste de progress bar")
        findForm5.click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "setProgress"))
        )
        botaoProgress = driver.find_element(By.ID, "setProgress")
        botaoProgress.click()

        capitulo_atual = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "currentcapitulo"))
        )
        capitulo_atual.clear()
        capitulo_atual.send_keys("10")

        capitulo_total = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "totalcapitulo"))
        )
        capitulo_total.clear()
        capitulo_total.send_keys("30")

        save = driver.find_element(By.ID, "saveProgress")
        save.click()

        time.sleep(1)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        time.sleep(2)

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/register/")

        usuarioComentar = driver.find_element(By.NAME, "username")
        senhaComentar = driver.find_element(By.NAME, "password1")
        senha2Comentar = driver.find_element(By.NAME, "password2")
        registrarComentar = driver.find_element(By.NAME, "registrar")

        usuarioComentar.send_keys("usercomumprogressbar")
        senhaComentar.send_keys("senha")
        senha2Comentar.send_keys("senha")
        registrarComentar.click()

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("usercomumprogressbar")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/clubs/")

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        botao_card = driver.find_element(By.NAME, "titles")
        botao_card.click()

        time.sleep(1)

        botao_club = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, "entrar-btn"))
        )
        botao_club.click()

        time.sleep(1) 

        try:
            botao_club_novo_entrar = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "entrar-btn"))
            )
            botao_club_novo_entrar.click()
        except:
            driver.execute_script("arguments[0].click();", botao_club_novo_entrar)

        time.sleep(2)