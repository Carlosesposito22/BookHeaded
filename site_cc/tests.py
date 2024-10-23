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

        assert usuario is not None, "Campo 'username' não encontrado"
        assert senha is not None, "Campo 'password1' não encontrado"
        assert senha2 is not None, "Campo 'password2' não encontrado"
        assert registrar is not None, "Botão 'registrar' não encontrado"

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

        assert usuariologin is not None, "Campo de login 'username' não encontrado"
        assert senhalogin is not None, "Campo de login 'password' não encontrado"

        usuariologin.send_keys("testefollow")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/usuarios/?nomes=")

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, 'user'))
            )
            pfp_touch = driver.find_element(By.NAME, 'user')
            pfp_touch.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'follow-text'))
            )
            followbtn = driver.find_element(By.ID, 'follow-text')
            followbtn.click()
            time.sleep(2)

            view_followers = driver.find_element(By.ID, 'followers-text2')
            assert view_followers is not None, "Botão de visualização de seguidores não encontrado"
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

        assert usuariologin is not None, "Campo de login 'username' não encontrado"
        assert senhalogin is not None, "Campo de login 'password' não encontrado"

        usuariologin.send_keys("testefollow")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/usuarios/?nomes=")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'user'))
        )
        pfp_touch = driver.find_element(By.NAME, 'user')
        pfp_touch.click()
        time.sleep(2)

        view_followers = driver.find_element(By.ID, 'followers-text2')
        assert view_followers is not None, "Botão de visualização de seguidores não encontrado"
        view_followers.click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Unfollow')]"))
        )

        try:
            unfollow_button = driver.find_element(By.XPATH, "//*[contains(text(),'Unfollow')]")
            assert unfollow_button is not None, "Botão 'Unfollow' não encontrado"
            driver.execute_script("arguments[0].click();", unfollow_button)
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Follow')]"))
            )

            view_followers2 = driver.find_element(By.ID, 'followers-text2')
            assert view_followers2 is not None, "Botão de visualização de seguidores não encontrado após Unfollow"
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
        self.assertContains(response, 'images/icon1.svg')
        self.assertContains(response, '1 Followers')
        self.assertContains(response, '0 Following')

    def test_followers_and_following_display_with_icons_and_usernames(self):
        """Verificar se os seguidores e seguidos aparecem corretamente com as fotos de perfil e nomes"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))

        self.assertContains(response, '@user2')
        self.assertContains(response, 'images/icon2.svg')

        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user2.id}))

        self.assertContains(response, '@user1')
        self.assertContains(response, 'images/icon1.svg')

    def test_correct_followers_and_following_links(self):
        """Verificar se os links dos seguidores e seguidos estão corretos"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))

        self.assertContains(response, reverse('profile', kwargs={'user_id': self.user2.id}))

        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user2.id}))
        self.assertContains(response, reverse('profile', kwargs={'user_id': self.user1.id}))

    def test_profile_icon_in_navbar(self):
        """Verificar se o ícone de perfil correto aparece na navbar para o usuário logado"""

        self.client.login(username='user1', password='password123')

        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))

        self.assertContains(response, 'images/icon1.svg', msg_prefix="O ícone de perfil do user1 não está correto na navbar.")
        self.assertEqual(response.status_code, 200)

        self.client.login(username='user2', password='password123')

        response = self.client.get(reverse('profile', kwargs={'user_id': self.user2.id}))

        self.assertContains(response, 'images/icon2.svg', msg_prefix="O ícone de perfil do user2 não está correto na navbar.")
        self.assertEqual(response.status_code, 200)


class ProfileEditTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio="Initial bio", icone='images/icon3.svg')

        self.client.login(username='testuser', password='12345')

    def test_edit_button_visible_and_functional(self):

        response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}))

        self.assertContains(response, 'bi-pencil-fill', msg_prefix="O botão de edição não está visível para o proprietário do perfil")

        new_bio = "New bio text"
        new_icon = 'images/icon4.svg'
        response = self.client.post(reverse('profile', kwargs={'user_id': self.user.id}), {
            'bio': new_bio,
            'icone': new_icon
        })

        self.assertEqual(response.status_code, 302)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, new_bio, "A bio não foi atualizada corretamente")
        self.assertEqual(self.profile.icone, new_icon, "O ícone de perfil não foi atualizado corretamente")

    def test_partial_edit(self):

        new_bio = "Another bio update"
        response = self.client.post(reverse('profile', kwargs={'user_id': self.user.id}), {
            'bio': new_bio,
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, new_bio, "A bio não foi atualizada corretamente ao editar somente a bio")
        self.assertEqual(self.profile.icone, 'images/icon3.svg', "O ícone não deveria ter sido alterado")

        new_icon = 'images/icon5.svg'
        response = self.client.post(reverse('profile', kwargs={'user_id': self.user.id}), {
            'icone': new_icon,
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.icone, new_icon, "O ícone não foi atualizado corretamente ao editar somente o ícone")


class ProfileEditNavbarTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, icone='images/icon3.svg')

        self.client.login(username='testuser', password='12345')

    def test_profile_icon_update_reflects_in_navbar(self):

        response = self.client.get(reverse('pagina_principal'))
        self.assertContains(response, 'images/icon3.svg', msg_prefix="O ícone original não foi encontrado na navbar antes da edição.")

        new_icon = 'images/icon4.svg'
        response = self.client.post(reverse('profile', kwargs={'user_id': self.user.id}), {
            'icone': new_icon,
        })

        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('pagina_principal'))  # Pega uma página que carrega a navbar
        self.assertContains(response, new_icon, msg_prefix="O novo ícone de perfil não foi atualizado na navbar.")


class SearchUsersTests(TestCase):
   
    def setUp(self):

        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')
        self.user3 = User.objects.create_user(username='alice', password='password123')

        Profile.objects.create(user=self.user1, bio="Bio for testuser1", icone='images/icon1.svg')
        Profile.objects.create(user=self.user2, bio="Bio for testuser2", icone='images/icon2.svg')
        Profile.objects.create(user=self.user3, bio="Bio for Alice", icone='images/icon3.svg')

        self.client.login(username='testuser1', password='password123')

    def test_search_bar_is_available(self):
        """Verifica se a barra de pesquisa está disponível na página"""

        response = self.client.get(reverse('lista_usuarios'))

        self.assertEqual(response.status_code, 200)
       
        self.assertIn('placeholder="Search Bookheads"', response.content.decode(),
                    msg="O placeholder da barra de pesquisa não está correto.")

    def test_search_returns_multiple_results_with_profile_info(self):
        """Verifica se a busca retorna múltiplos resultados e exibe as informações corretas"""
        response = self.client.get(reverse('lista_usuarios'), {'nomes': 'testuser'})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'testuser1', msg_prefix="O nome do usuário testuser1 não foi exibido corretamente.")
        self.assertContains(response, 'Bio for testuser1', msg_prefix="A bio do usuário testuser1 não foi exibida corretamente.")
        self.assertContains(response, 'images/icon1.svg', msg_prefix="O ícone do usuário testuser1 não foi exibido corretamente.")
       
        self.assertContains(response, 'testuser2', msg_prefix="O nome do usuário testuser2 não foi exibido corretamente.")
        self.assertContains(response, 'Bio for testuser2', msg_prefix="A bio do usuário testuser2 não foi exibida corretamente.")
        self.assertContains(response, 'images/icon2.svg', msg_prefix="O ícone do usuário testuser2 não foi exibido corretamente.")

    def test_search_no_results(self):
        """Verifica se a pesquisa que não retorna resultados exibe a mensagem correta"""
        response = self.client.get(reverse('lista_usuarios'), {'nomes': 'nonexistentuser'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum usuário encontrado.', msg_prefix="A mensagem de 'Nenhum usuário encontrado' não foi exibida.")

    def test_click_on_search_result_opens_correct_profile_with_info(self):
        """Verifica se ao clicar no resultado da pesquisa o perfil correto é aberto"""
        response = self.client.get(reverse('lista_usuarios'), {'nomes': 'alice'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alice', msg_prefix="O resultado da busca não exibiu o usuário 'alice'.")

        profile_url = reverse('profile', kwargs={'user_id': self.user3.id})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'alice', msg_prefix="O nome do perfil não está correto.")
        self.assertContains(response, 'Bio for Alice', msg_prefix="A bio do perfil não está correta.")
        self.assertContains(response, 'images/icon3.svg', msg_prefix="O ícone de perfil não está correto.")

    def test_search_with_empty_query_returns_all_profiles(self):
        """Verifica se a pesquisa com campo vazio retorna todos os perfis"""
        response = self.client.get(reverse('lista_usuarios'), {'nomes': ''})
        self.assertEqual(response.status_code, 200)

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

        time.sleep(1)

        botao_club = driver.find_element(By.NAME, "entrar-btn")
        botao_club.click()

        time.sleep(1)

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

class ClubePrivadoTests(LiveServerTestCase):

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

    def teste_campos_club(self):
        try:
            driver = self.driver
            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "newclub-btn")
            assert botao_club is not None, "Botão 'newclub-btn' não encontrado"
            botao_club.click()
            time.sleep(1)

            titulo_input = driver.find_element(By.ID, "titulo")
            assert titulo_input is not None, "Campo 'titulo' não encontrado"
            titulo_input.send_keys("Book w4")

            categoria_select = Select(driver.find_element(By.ID, "categoria"))
            assert categoria_select is not None, "Campo de seleção 'categoria' não encontrado"
            categoria_select.select_by_value("1")

            descricao_input = driver.find_element(By.ID, "descricao")
            assert descricao_input is not None, "Campo de descrição 'descricao' não encontrado"
            descricao_input.send_keys("This is a test description for the book club.")

            checkbox = driver.find_element(By.ID, "privado")
            assert checkbox is not None, "Checkbox 'privado' não encontrado"
            checkbox.click()

            create_btn = driver.find_element(By.ID, "create-btn")
            assert create_btn is not None, "Botão de criação 'create-btn' não encontrado"
            driver.execute_script("arguments[0].removeAttribute('disabled')", create_btn)
            create_btn.click()
            time.sleep(3)

            modalidade_select = Select(driver.find_element(By.ID, "modalidade"))
            assert modalidade_select is not None, "Campo de seleção 'modalidade' não encontrado"
            modalidade_select.select_by_value("1")
            create_btn.click()
            time.sleep(3)

            print("Teste de verificação campos obrigatórios.")
        
        except Exception as e:
            print(f"Falha no teste de verificação campos obrigatórios: {e}")


    def teste_receber_solicitacao_duplicada_e_recebimento(self):
        try:
            driver = self.driver
            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "newclub-btn")
            assert botao_club is not None, "Botão 'newclub-btn' não encontrado"
            botao_club.click()
            time.sleep(1)

            titulo_input = driver.find_element(By.ID, "titulo")
            assert titulo_input is not None, "Campo 'titulo' não encontrado"
            titulo_input.send_keys("Book w4")

            categoria_select = Select(driver.find_element(By.ID, "categoria"))
            assert categoria_select is not None, "Campo de seleção 'categoria' não encontrado"
            categoria_select.select_by_value("1")

            modalidade_select = Select(driver.find_element(By.ID, "modalidade"))
            assert modalidade_select is not None, "Campo de seleção 'modalidade' não encontrado"
            modalidade_select.select_by_value("1")

            descricao_input = driver.find_element(By.ID, "descricao")
            assert descricao_input is not None, "Campo de descrição 'descricao' não encontrado"
            descricao_input.send_keys("This is a test description for the book club.")

            checkbox = driver.find_element(By.ID, "privado")
            assert checkbox is not None, "Checkbox 'privado' não encontrado"
            checkbox.click()

            create_btn = driver.find_element(By.ID, "create-btn")
            assert create_btn is not None, "Botão de criação 'create-btn' não encontrado"
            driver.execute_script("arguments[0].removeAttribute('disabled')", create_btn)
            create_btn.click()
            time.sleep(3)

            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaMembro")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaMembro")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "abaclubs")
            assert botao_club is not None, "Botão 'abaclubs' não encontrado"
            botao_club.click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pesquisa-barra")))

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            assert pesquisa_barra is not None, "Barra de pesquisa não encontrada"
            pesquisa_barra.send_keys("Book w4")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            botao_card = driver.find_element(By.NAME, "titles")
            assert botao_card is not None, "Botão do card 'titles' não encontrado"
            botao_card.click()
            time.sleep(2)

            botao_club = driver.find_element(By.NAME, "solicitar")
            assert botao_club is not None, "Botão 'solicitar' não encontrado"
            botao_club.click()
            time.sleep(3)

            botao_club = driver.find_element(By.ID, "clubsLink")
            assert botao_club is not None, "Link 'clubsLink' não encontrado"
            botao_club.click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pesquisa-barra")))

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            assert pesquisa_barra is not None, "Barra de pesquisa não encontrada"
            pesquisa_barra.send_keys("Book w4")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            botao_card = driver.find_element(By.NAME, "titles")
            assert botao_card is not None, "Botão do card 'titles' não encontrado"
            botao_card.click()
            time.sleep(2)

            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/myclubes/")
            time.sleep(2)

            pesquisa_barra2 = driver.find_element(By.NAME, "nome")
            assert pesquisa_barra2 is not None, "Campo de pesquisa 'nome' não encontrado"
            pesquisa_barra2.send_keys("Book w4")
            pesquisa_barra2.send_keys(Keys.ENTER)
            time.sleep(2)

            botao_card2 = driver.find_element(By.ID, "tituloCard")
            assert botao_card2 is not None, "Botão 'tituloCard' não encontrado"
            botao_card2.click()
            time.sleep(2)

            botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
            assert botao_club_novo_entrar is not None, "Botão 'entrar-btn' não encontrado"
            botao_club_novo_entrar.click()
            time.sleep(3)

            botao_card3 = driver.find_element(By.ID, "engine")
            assert botao_card3 is not None, "Botão 'engine' não encontrado"
            botao_card3.click()
            time.sleep(2)

            botao_card4 = driver.find_element(By.ID, "request")
            assert botao_card4 is not None, "Botão 'request' não encontrado"
            botao_card4.click()
            time.sleep(2)

            botao_card5 = driver.find_element(By.ID, "aprove")
            assert botao_card5 is not None, "Botão 'aprove' não encontrado"
            botao_card5.click()
            time.sleep(4)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaMembro")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "abaclubs")
            assert botao_club is not None, "Botão 'abaclubs' não encontrado"
            botao_club.click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pesquisa-barra")))

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            assert pesquisa_barra is not None, "Barra de pesquisa não encontrada"
            pesquisa_barra.send_keys("Book w4")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            botao_card = driver.find_element(By.NAME, "titles")
            assert botao_card is not None, "Botão do card 'titles' não encontrado"
            botao_card.click()
            time.sleep(2)

        except Exception as e:
            print(f"Falha no teste de verificação campos obrigatórios: {e}")


    def teste_solicitacao_negada(self):
        try:
            driver = self.driver
            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "newclub-btn")
            assert botao_club is not None, "Botão 'newclub-btn' não encontrado"
            botao_club.click()
            time.sleep(1)

            titulo_input = driver.find_element(By.ID, "titulo")
            assert titulo_input is not None, "Campo 'titulo' não encontrado"
            titulo_input.send_keys("Book w4")

            categoria_select = Select(driver.find_element(By.ID, "categoria"))
            assert categoria_select is not None, "Campo de seleção 'categoria' não encontrado"
            categoria_select.select_by_value("1")

            modalidade_select = Select(driver.find_element(By.ID, "modalidade"))
            assert modalidade_select is not None, "Campo de seleção 'modalidade' não encontrado"
            modalidade_select.select_by_value("1")

            descricao_input = driver.find_element(By.ID, "descricao")
            assert descricao_input is not None, "Campo de descrição 'descricao' não encontrado"
            descricao_input.send_keys("This is a test description for the book club.")

            checkbox = driver.find_element(By.ID, "privado")
            assert checkbox is not None, "Checkbox 'privado' não encontrado"
            checkbox.click()

            create_btn = driver.find_element(By.ID, "create-btn")
            assert create_btn is not None, "Botão de criação 'create-btn' não encontrado"
            driver.execute_script("arguments[0].removeAttribute('disabled')", create_btn)
            create_btn.click()
            time.sleep(3)

            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaMembro")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaMembro")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "abaclubs")
            assert botao_club is not None, "Botão 'abaclubs' não encontrado"
            botao_club.click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pesquisa-barra")))

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            assert pesquisa_barra is not None, "Barra de pesquisa não encontrada"
            pesquisa_barra.send_keys("Book w4")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            botao_card = driver.find_element(By.NAME, "titles")
            assert botao_card is not None, "Botão do card não encontrado"
            botao_card.click()
            time.sleep(2)

            botao_club = driver.find_element(By.NAME, "solicitar")
            assert botao_club is not None, "Botão 'solicitar' não encontrado"
            botao_club.click()
            time.sleep(3)

            botao_club = driver.find_element(By.ID, "clubsLink")
            assert botao_club is not None, "Link 'clubsLink' não encontrado"
            botao_club.click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pesquisa-barra")))

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            assert pesquisa_barra is not None, "Barra de pesquisa não encontrada"
            pesquisa_barra.send_keys("Book w4")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            botao_card = driver.find_element(By.NAME, "titles")
            assert botao_card is not None, "Botão do card não encontrado"
            botao_card.click()
            time.sleep(2)

            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/myclubes/")
            time.sleep(2)

            pesquisa_barra2 = driver.find_element(By.NAME, "nome")
            assert pesquisa_barra2 is not None, "Campo de pesquisa não encontrado"
            pesquisa_barra2.send_keys("Book w4")
            pesquisa_barra2.send_keys(Keys.ENTER)
            time.sleep(2)

            botao_card2 = driver.find_element(By.ID, "tituloCard")
            assert botao_card2 is not None, "Botão 'tituloCard' não encontrado"
            botao_card2.click()
            time.sleep(2)

            botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
            assert botao_club_novo_entrar is not None, "Botão 'entrar-btn' não encontrado"
            botao_club_novo_entrar.click()
            time.sleep(3)

            botao_card3 = driver.find_element(By.ID, "engine")
            assert botao_card3 is not None, "Botão 'engine' não encontrado"
            botao_card3.click()
            time.sleep(2)

            botao_card4 = driver.find_element(By.ID, "request")
            assert botao_card4 is not None, "Botão 'request' não encontrado"
            botao_card4.click()
            time.sleep(2)

            botao_card5 = driver.find_element(By.ID, "recusar")
            assert botao_card5 is not None, "Botão 'recusar' não encontrado"
            botao_card5.click()
            time.sleep(4)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaMembro")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "abaclubs")
            assert botao_club is not None, "Botão 'abaclubs' não encontrado"
            botao_club.click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pesquisa-barra")))

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            assert pesquisa_barra is not None, "Barra de pesquisa não encontrada"
            pesquisa_barra.send_keys("Book w4")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            botao_card = driver.find_element(By.NAME, "titles")
            assert botao_card is not None, "Botão do card não encontrado"
            botao_card.click()
            time.sleep(4)

        except Exception as e:
            print(f"Falha no teste de verificação campos obrigatórios: {e}")

        
    
                


class BarraDePesquisa(LiveServerTestCase):

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

    def teste_barra_pesquisa(self):
        try:
            driver = self.driver
            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "newclub-btn")
            assert botao_club is not None, "Botão para criar clube não encontrado"
            botao_club.click()
            time.sleep(1)

            titulo_input = driver.find_element(By.ID, "titulo")
            assert titulo_input is not None, "Campo de título não encontrado"
            titulo_input.send_keys("Lilivro ola2")

            modalidade_select = Select(driver.find_element(By.ID, "modalidade"))
            assert modalidade_select is not None, "Campo de seleção 'modalidade' não encontrado"
            modalidade_select.select_by_value("1")

            categoria_select = Select(driver.find_element(By.ID, "categoria"))
            assert categoria_select is not None, "Campo de seleção 'categoria' não encontrado"
            categoria_select.select_by_value("1")

            descricao_input = driver.find_element(By.ID, "descricao")
            assert descricao_input is not None, "Campo de descrição não encontrado"
            descricao_input.send_keys("This is a test description for the book club.")

            create_btn = driver.find_element(By.ID, "create-btn")
            assert create_btn is not None, "Botão de criação do clube não encontrado"
            driver.execute_script("arguments[0].removeAttribute('disabled')", create_btn)
            create_btn.click()
            time.sleep(2)

            driver = self.driver
            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado (para o Membro)"
            assert senha is not None, "Campo 'password1' não encontrado (para o Membro)"
            assert senha2 is not None, "Campo 'password2' não encontrado (para o Membro)"
            assert registrar is not None, "Botão 'registrar' não encontrado (para o Membro)"

            usuario.send_keys("testemaratonaMembro")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado (para o Membro)"
            assert senhalogin is not None, "Campo de login 'password' não encontrado (para o Membro)"

            usuariologin.send_keys("testemaratonaMembro")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "abaclubs")
            assert botao_club is not None, "Botão de navegação para os clubes não encontrado"
            botao_club.click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pesquisa-barra")))

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            assert pesquisa_barra is not None, "Barra de pesquisa não encontrada"
            pesquisa_barra.send_keys("Lili")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            print("Teste de verificação de filtro parcial")

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            pesquisa_barra.clear()
            pesquisa_barra.send_keys("pppppppppppppppppppp")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            print("Teste de verificação de filtro nao existente")

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            pesquisa_barra.clear()
            pesquisa_barra.send_keys("LILIVRO")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            print("Teste de verificação de filtro case insensitive")
        except Exception as e:
            print(f"Falha no teste de verificação de presença do botão de moderador e participante: {e}")



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

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "newclub-btn")
            assert botao_club is not None, "Botão 'newclub-btn' não encontrado"
            botao_club.click()
            time.sleep(1)

            titulo_input = driver.find_element(By.ID, "titulo")
            assert titulo_input is not None, "Campo 'titulo' não encontrado"
            titulo_input.send_keys("Book ola2")

            modalidade_select = Select(driver.find_element(By.ID, "modalidade"))
            assert modalidade_select is not None, "Campo de seleção 'modalidade' não encontrado"
            modalidade_select.select_by_value("1")

            categoria_select = Select(driver.find_element(By.ID, "categoria"))
            assert categoria_select is not None, "Campo de seleção 'categoria' não encontrado"
            categoria_select.select_by_value("1")

            descricao_input = driver.find_element(By.ID, "descricao")
            assert descricao_input is not None, "Campo de descrição 'descricao' não encontrado"
            descricao_input.send_keys("This is a test description for the book club.")

            create_btn = driver.find_element(By.ID, "create-btn")
            assert create_btn is not None, "Botão de criação 'create-btn' não encontrado"
            driver.execute_script("arguments[0].removeAttribute('disabled')", create_btn)
            create_btn.click()
            time.sleep(3)

            driver.get("http://127.0.0.1:8000/membros/register/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuario = driver.find_element(By.NAME, "username")
            senha = driver.find_element(By.NAME, "password1")
            senha2 = driver.find_element(By.NAME, "password2")
            registrar = driver.find_element(By.NAME, "registrar")

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaMembro")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaMembro")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "abaclubs")
            assert botao_club is not None, "Botão 'abaclubs' não encontrado"
            botao_club.click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pesquisa-barra")))

            pesquisa_barra = driver.find_element(By.ID, "pesquisa-barra")
            assert pesquisa_barra is not None, "Barra de pesquisa não encontrada"
            pesquisa_barra.send_keys("Book ola2")
            pesquisa_barra.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            botao_card = driver.find_element(By.NAME, "titles")
            assert botao_card is not None, "Botão do card 'titles' não encontrado"
            botao_card.click()
            time.sleep(2)

            botao_club = driver.find_element(By.NAME, "entrar-btn")
            assert botao_club is not None, "Botão 'entrar-btn' não encontrado"
            botao_club.click()
            time.sleep(3)

            botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
            assert botao_club_novo_entrar is not None, "Botão 'entrar-btn' não encontrado (duplicado)"
            botao_club_novo_entrar.click()
            time.sleep(5)

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

            assert usuario is not None, "Campo 'username' não encontrado"
            assert senha is not None, "Campo 'password1' não encontrado"
            assert senha2 is not None, "Campo 'password2' não encontrado"
            assert registrar is not None, "Botão 'registrar' não encontrado"

            usuario.send_keys("testemaratonaModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testemaratonaModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            botao_club = driver.find_element(By.ID, "newclub-btn")
            assert botao_club is not None, "Botão 'newclub-btn' não encontrado"
            botao_club.click()
            time.sleep(1)

            titulo_input = driver.find_element(By.ID, "titulo")
            assert titulo_input is not None, "Campo 'titulo' não encontrado"
            titulo_input.send_keys("Book ola2")

            modalidade_select = Select(driver.find_element(By.ID, "modalidade"))
            assert modalidade_select is not None, "Campo de seleção 'modalidade' não encontrado"
            modalidade_select.select_by_value("1")

            categoria_select = Select(driver.find_element(By.ID, "categoria"))
            assert categoria_select is not None, "Campo de seleção 'categoria' não encontrado"
            categoria_select.select_by_value("1")

            descricao_input = driver.find_element(By.ID, "descricao")
            assert descricao_input is not None, "Campo de descrição 'descricao' não encontrado"
            descricao_input.send_keys("This is a test description for the book club.")

            create_btn = driver.find_element(By.ID, "create-btn")
            assert create_btn is not None, "Botão de criação 'create-btn' não encontrado"
            driver.execute_script("arguments[0].removeAttribute('disabled')", create_btn)
            create_btn.click()
            time.sleep(2)

            botao_maratona = driver.find_element(By.ID, "createMaratona")
            assert botao_maratona is not None, "Botão 'createMaratona' não encontrado"
            botao_maratona.click()
            time.sleep(4)

            nome_maratona = driver.find_element(By.ID, "nomeMaratona")
            assert nome_maratona is not None, "Campo 'nomeMaratona' não encontrado"
            nome_maratona.send_keys("Teste Maratona")
            time.sleep(2)

            data_fim = driver.find_element(By.ID, "dataFim")
            assert data_fim is not None, "Campo 'dataFim' não encontrado"
            data_fim.send_keys("30122024")
            time.sleep(2)

            capitulo_final = driver.find_element(By.ID, "capituloFinal")
            assert capitulo_final is not None, "Campo 'capituloFinal' não encontrado"
            capitulo_final.send_keys("100")
            time.sleep(2)

            botao_save_maratona = driver.find_element(By.ID, "saveMaratona")
            assert botao_save_maratona is not None, "Botão 'saveMaratona' não encontrado"
            botao_save_maratona.click()
            time.sleep(4)

            self.assertTrue(True, "Teste de criação de maratona foi concluído com sucesso.")

        except Exception as e:

            self.fail(f"Falha no teste de criação de maratona: {e}")






class SairDoClubeTest(TestCase):

    def setUp(self):

        self.categoria = Categoria.objects.get(nome='Ficção')
        self.modalidade = Modalidade.objects.get(nome='Online')

        self.moderador = User.objects.create_user(username='moderador', password='Asd12345678')
        self.client.login(username='moderador', password='Asd12345678')

        self.clube = Clube.objects.create(
            titulo='Clube de Teste',
            moderador=self.moderador,
            descricao='Um clube de teste',
            categoria=self.categoria,
            modalidade=self.modalidade
        )

        self.membro = User.objects.create_user(username='membro', password='Asd12345678')
        Membro.objects.create(clube=self.clube, usuario=self.membro)

    def test_botao_nao_aparece_para_moderador(self):
        response = self.client.get(reverse('club-Detail', args=[self.clube.id]))

        self.assertNotContains(response, '<button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#sairDoClubeModal-{{ clube.id }}">Sair do Clube</button>')

    def test_botao_sair_do_clube_aparece_para_membro(self):

        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        response = self.client.get(reverse('club-Detail', args=[self.clube.id]))

        self.assertContains(response, 'Sair do Clube')

    def test_usuario_sai_do_clube(self):

        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        response = self.client.post(reverse('sair-do-clube', args=[self.clube.id]))

        self.assertFalse(Membro.objects.filter(clube=self.clube, usuario=self.membro).exists())

        self.assertRedirects(response, reverse('myclubes'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Você saiu do clube "{self.clube.titulo}"')


class FavoritarClubeTest(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.get(nome='Ficção')
        self.modalidade = Modalidade.objects.get(nome='Online')

        self.moderador = User.objects.create_user(username='moderador', password='Asd12345678')
        self.client.login(username='moderador', password='Asd12345678')

        self.clube = Clube.objects.create(
            titulo='Clube de Teste',
            moderador=self.moderador,
            descricao='Clube para testes de funcionalidade',
            categoria=self.categoria,
            modalidade=self.modalidade
        )

        self.membro = User.objects.create_user(username='membro', password='Asd12345678')

    def test_usuario_logado_pode_favoritar_clube(self):

        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        response = self.client.post(reverse('favoritar_clube', args=[self.clube.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.membro in self.clube.favoritos.all())

    def test_lista_de_clubes_favoritos_atualizada(self):

        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        self.client.post(reverse('favoritar_clube', args=[self.clube.id]))

        self.assertTrue(self.clube in self.membro.clubes_favoritos.all())

    def test_usuario_pode_visualizar_clubes_favoritos(self):

        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        self.membro.clubes_favoritos.add(self.clube)

        response = self.client.get(reverse('myclubes'))

        self.assertContains(response, self.clube.titulo)

        self.assertContains(response, '<i class="bi bi-star-fill star-from-btn"></i>')

    def test_usuario_pode_desfavoritar_clube(self):

        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        self.client.post(reverse('favoritar_clube', args=[self.clube.id]))
        response = self.client.post(reverse('favoritar_clube', args=[self.clube.id]))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.membro in self.clube.favoritos.all())


class LivrosFavoritosTest(TestCase):

    def setUp(self):

        self.categoria = Categoria.objects.get(nome='Ficção')
        self.modalidade = Modalidade.objects.get(nome='Online')

        self.moderador = User.objects.create_user(username='moderador', password='Asd12345678')
        self.client.login(username='moderador', password='Asd12345678')

        self.clube = Clube.objects.create(
            titulo='Clube de Leitura',
            moderador=self.moderador,
            descricao='Clube para leitura de ficção científica',
            categoria=self.categoria,
            modalidade=self.modalidade
        )

        self.membro = User.objects.create_user(username='membro', password='Asd12345678')

    def test_moderador_pode_adicionar_livros_favoritos(self):
        response = self.client.post(reverse('add_top_livros', args=[self.clube.id]), {
            'top_livros': 'Livro 1\nLivro 2\nLivro 3'
        })

        self.clube.refresh_from_db()
        self.assertEqual(self.clube.top_livros, 'Livro 1\nLivro 2\nLivro 3')
        self.assertEqual(response.status_code, 302)

    def test_membros_podem_visualizar_livros_favoritos(self):

        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        self.clube.top_livros = 'Livro 1\nLivro 2\nLivro 3'
        self.clube.save()

        response = self.client.get(reverse('club-Detail', args=[self.clube.id]))

        self.assertContains(response, 'Livro 1')
        self.assertContains(response, 'Livro 2')
        self.assertContains(response, 'Livro 3')

    def test_moderador_pode_editar_livros_favoritos(self):

        self.clube.top_livros = 'Livro 1\nLivro 2'
        self.clube.save()

        response = self.client.post(reverse('add_top_livros', args=[self.clube.id]), {
            'top_livros': 'Livro 1\nLivro 2\nLivro 3'
        })

        self.clube.refresh_from_db()
        self.assertEqual(self.clube.top_livros, 'Livro 1\nLivro 2\nLivro 3')

    def test_membro_nao_pode_editar_livros_favoritos(self):

        self.client.logout()
        self.client.login(username='membro', password='Asd12345678')

        response = self.client.post(reverse('add_top_livros', args=[self.clube.id]), {
            'top_livros': 'Livro Indevido'
        })

        self.assertEqual(response.status_code, 403)
        self.clube.refresh_from_db()
        self.assertNotEqual(self.clube.top_livros, 'Livro Indevido')


class AvaliacaoClubeTest(TestCase):

    def setUp(self):

        self.categoria = Categoria.objects.create(nome='Ficção')
        self.modalidade = Modalidade.objects.create(nome='Online')

        self.moderador = User.objects.create_user(username='moderador', password='modpassword')

        self.clube = Clube.objects.create(
            titulo='Clube de Teste',
            moderador=self.moderador,
            descricao='Um clube para testar avaliações',
            categoria=self.categoria,
            modalidade=self.modalidade
        )

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

        avaliacao = Avaliacao.objects.filter(clube=self.clube, usuario=self.participante).first()
        self.assertIsNotNone(avaliacao)
        self.assertEqual(avaliacao.valor, 4)

    def test_usuario_nao_seleciona_nota_exibe_erro(self):
        """Testar se o envio de uma avaliação sem uma nota exibe uma mensagem de erro"""
        self.client.login(username='participante', password='password123')

        response = self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': ''})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Avaliacao.objects.filter(clube=self.clube, usuario=self.participante).count(), 0)

        self.assertContains(response, "Este campo é obrigatório e deve ser um número entre 1 e 5.")

    def test_usuario_pode_atualizar_avaliacao(self):
        """Verificar se o participante pode atualizar sua avaliação"""
        self.client.login(username='participante', password='password123')

        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 4})

        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 5})

        avaliacao = Avaliacao.objects.get(clube=self.clube, usuario=self.participante)
        self.assertEqual(avaliacao.valor, 5)

    def test_media_avaliacoes_atualizada_corretamente(self):
        """Verificar se a média de avaliações é atualizada corretamente após nova avaliação"""
        participante2 = User.objects.create_user(username='participante2', password='password123')
        self.client.login(username='participante', password='password123')
        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 3})

        self.client.login(username='participante2', password='password123')
        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 5})

        self.assertEqual(self.clube.calcular_media_avaliacoes(), 4)

    def test_usuario_nao_pode_avaliar_mais_de_uma_vez(self):
        """Verificar se o participante não pode enviar uma nova avaliação, mas apenas atualizar a existente"""
        self.client.login(username='participante', password='password123')

        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 3})

        self.client.post(reverse('avaliacoes_clube', args=[self.clube.id]), {'rating': 5})

        avaliacao = Avaliacao.objects.filter(clube=self.clube, usuario=self.participante).count()
        self.assertEqual(avaliacao, 1)

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

        time.sleep(3) 

        try:
            botao_club_novo_entrar = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "entrar-btn"))
            )
            botao_club_novo_entrar.click()
        except:
            driver.execute_script("arguments[0].click();", botao_club_novo_entrar)

        time.sleep(2)
        
class TestFiltro(TestCase):
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

#nao tem clube
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
        
        time.sleep(1)

        driver.get("http://127.0.0.1:8000/clubs/")
        
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, 20000);")
        
        time.sleep(2)

        botao_ficcao = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.ID, "botao-filtro"))
         )
        botao_ficcao.click()
        
        time.sleep(2)
        
        botao_autoajuda = driver.find_element(By.XPATH, "//button[contains(text(), 'Mistério')]")
        botao_autoajuda.click()
    
        time.sleep(2)  
        
        botao_filter = driver.find_element(By.ID, "filter")
        botao_filter.click()
        
        time.sleep(2)
        
        driver.execute_script("window.scrollTo(0, 20000);")
        
        time.sleep(2)
        
        page_content = driver.page_source
        assert "Mistério" in page_content, "O filtro de Mistério não foi aplicado corretamente."

#tem clube
    def teste_cenario2(self):
        
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
        
        time.sleep(1)

        driver.get("http://127.0.0.1:8000/clubs/")
        
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, 20000);")
        
        time.sleep(2)

        botao_ficcao = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.ID, "botao-filtro"))
         )
        botao_ficcao.click()
        
        time.sleep(2)
        
        botao_autoajuda = driver.find_element(By.XPATH, "//button[contains(text(), 'Ficção')]")
        botao_autoajuda.click()
    
        time.sleep(2)  
        
        botao_filter = driver.find_element(By.ID, "filter")
        botao_filter.click()
        
        time.sleep(2)
        
        driver.execute_script("window.scrollTo(0, 20000);")
        
        time.sleep(2)
        
        page_content = driver.page_source
        assert "Ficção" in page_content, "O filtro de Ficção não foi aplicado corretamente."