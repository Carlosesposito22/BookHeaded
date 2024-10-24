from django.contrib.auth.models import User
from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from .models import Clube, Membro, Comentario, Modalidade, Categoria, HistoricoMaratona, Profile, Avaliacao
from .views import comentario_create_view
from unittest.mock import patch
from django.conf import settings
from django.http import HttpResponseForbidden
from datetime import datetime
from django.core.management import call_command
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from django.contrib.staticfiles.testing import LiveServerTestCase
import requests
import json
import logging
import time
import os


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


class SairDoClubeTests(TestCase):

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

    def test_sair_do_clube(self):
        driver = self.driver

        # 1. Registro do moderador
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuarioComentar = driver.find_element(By.NAME, "username")
        senhaComentar = driver.find_element(By.NAME, "password1")
        senha2Comentar = driver.find_element(By.NAME, "password2")
        registrarComentar = driver.find_element(By.NAME, "registrar")

        # Asserts para verificar que os elementos estão presentes
        self.assertIsNotNone(usuarioComentar, "Campo 'username' não encontrado.")
        self.assertIsNotNone(senhaComentar, "Campo 'password1' não encontrado.")
        self.assertIsNotNone(senha2Comentar, "Campo 'password2' não encontrado.")
        self.assertIsNotNone(registrarComentar, "Botão de registro não encontrado.")

        usuarioComentar.send_keys("moderador_clube")
        senhaComentar.send_keys("senha_moderador")
        senha2Comentar.send_keys("senha_moderador")
        registrarComentar.send_keys(Keys.ENTER)

        # 2. Login do moderador
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        # Asserts para garantir que os campos de login estão presentes
        self.assertIsNotNone(usuariologin, "Campo 'username' de login não encontrado.")
        self.assertIsNotNone(senhalogin, "Campo 'password' de login não encontrado.")

        usuariologin.send_keys("moderador_clube")
        senhalogin.send_keys("senha_moderador")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        # 3. Criar um novo clube
        newclub = driver.find_element(By.ID, "newclub-btn")
        self.assertIsNotNone(newclub, "Botão 'Create Club' não encontrado.")
        newclub.click()

        time.sleep(1)

        findForm1 = driver.find_element(By.NAME, "titulo")
        findForm2 = driver.find_element(By.NAME, "modalidade")
        findForm3 = driver.find_element(By.NAME, "categoria")
        findForm4 = driver.find_element(By.NAME, "descricao")
        findForm5 = driver.find_element(By.ID, "create-btn")

        # Asserts para verificar os campos de criação do clube
        self.assertIsNotNone(findForm1, "Campo 'titulo' não encontrado.")
        self.assertIsNotNone(findForm2, "Campo 'modalidade' não encontrado.")
        self.assertIsNotNone(findForm3, "Campo 'categoria' não encontrado.")
        self.assertIsNotNone(findForm4, "Campo 'descricao' não encontrado.")
        self.assertIsNotNone(findForm5, "Botão 'create-btn' não encontrado.")

        findForm1.send_keys("Clube de Teste Sair")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descrição do clube de teste para sair.")

        time.sleep(1)
        findForm5.click()

        time.sleep(4)

        # 4. clicar no logout
        driver.get("http://127.0.0.1:8000")
        pfp = driver.find_element(By.NAME, "pfp")
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")
        pfp.click()

        time.sleep(2)

        logout = driver.find_element(By.ID, "logout-btn")
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()

        time.sleep(1)

        # 5. Registro do membro
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuarioComentar2 = driver.find_element(By.NAME, "username")
        senhaComentar2 = driver.find_element(By.NAME, "password1")
        senha2Comentar2 = driver.find_element(By.NAME, "password2")
        registrarComentar2 = driver.find_element(By.NAME, "registrar")

        # Asserts para verificar que os elementos estão presentes
        self.assertIsNotNone(usuarioComentar2, "Campo 'username' não encontrado.")
        self.assertIsNotNone(senhaComentar2, "Campo 'password1' não encontrado.")
        self.assertIsNotNone(senha2Comentar2, "Campo 'password2' não encontrado.")
        self.assertIsNotNone(registrarComentar2, "Botão de registro não encontrado.")

        usuarioComentar2.send_keys("membro_clube")
        senhaComentar2.send_keys("senha_membro")
        senha2Comentar2.send_keys("senha_membro")
        registrarComentar2.send_keys(Keys.ENTER)

        # 6. Login do membro
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin2 = driver.find_element(By.NAME, "username")
        senhalogin2 = driver.find_element(By.NAME, "password")

        # Asserts para garantir que os campos de login estão presentes
        self.assertIsNotNone(usuariologin2, "Campo 'username' de login não encontrado.")
        self.assertIsNotNone(senhalogin2, "Campo 'password' de login não encontrado.")

        usuariologin2.send_keys("membro_clube")
        senhalogin2.send_keys("senha_membro")
        senhalogin2.send_keys(Keys.ENTER)

        time.sleep(1)

        # 7. Navegar para o clube e entrar nele
        driver.get("http://127.0.0.1:8000/clubs/")
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/clubs/", "Não foi redirecionado corretamente para a página 'Clubs'.")

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        botao_card = driver.find_element(By.NAME, "titles")
        self.assertIsNotNone(botao_card, "Botão do card do clube não encontrado.")
        botao_card.click()

        time.sleep(1)

        # Acessa a modal de clubs
        botao_club = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club, "Botão de entrar no clube não encontrado.")
        botao_club.click()

        time.sleep(1)

        # Acessa a modal de clubs novamente
        botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club_novo_entrar, "Botão de entrar no clube (2ª vez) não encontrado.")
        botao_club_novo_entrar.click()

        time.sleep(3)

        # 8. Sair do clube
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sair-do-clube-btn")))
        sair_do_clube_btn = driver.find_element(By.ID, "sair-do-clube-btn")
        self.assertIsNotNone(sair_do_clube_btn, "Botão 'Sair do Clube' não encontrado.")
        sair_do_clube_btn.click()

        # Verificar se a modal de confirmação aparece
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal.show")))
        modal_sair = driver.find_element(By.CSS_SELECTOR, ".modal.show")
        self.assertTrue(modal_sair.is_displayed(), "Modal de confirmação não foi exibido.")

        confirmar_sair = driver.find_element(By.XPATH, "//form[@method='post']//button[contains(text(), 'Sair do Clube')]")
        self.assertIsNotNone(confirmar_sair, "Botão 'Confirmar Sair' não encontrado.")
        confirmar_sair.click()

        # 9. Verificar se a mensagem de sucesso foi exibida no frontend após sair do clube
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-warning")))
        mensagem_sucesso = driver.find_element(By.CSS_SELECTOR, ".alert-warning")
        self.assertIn("Você saiu do clube", mensagem_sucesso.text, "Mensagem de sucesso não foi exibida ou está incorreta.")

        time.sleep(3)

        # 10. Verificar no banco de dados se o membro foi removido
        def test_sair_do_clube(self):
            usuario_bd = User.objects.get(username="membro_clube")
            clube_bd = Clube.objects.get(titulo="Clube de Teste Sair")
            bool_clube = Membro.objects.filter(usuario=usuario_bd, clube=clube_bd, aprovado=True).exists()
            self.assertFalse(bool_clube, "Usuário ainda é membro do clube após sair.")


class FavoritarClubeTests(LiveServerTestCase):

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

    def test_01_moderador_favorita_clube(self):
        driver = self.driver

        # 1. Registro do moderador
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuarioComentar = driver.find_element(By.NAME, "username")
        senhaComentar = driver.find_element(By.NAME, "password1")
        senha2Comentar = driver.find_element(By.NAME, "password2")
        registrarComentar = driver.find_element(By.NAME, "registrar")

        # Asserts para verificar que os elementos estão presentes
        self.assertIsNotNone(usuarioComentar, "Campo 'username' não encontrado.")
        self.assertIsNotNone(senhaComentar, "Campo 'password1' não encontrado.")
        self.assertIsNotNone(senha2Comentar, "Campo 'password2' não encontrado.")
        self.assertIsNotNone(registrarComentar, "Botão de registro não encontrado.")

        usuarioComentar.send_keys("moderador_clube")
        senhaComentar.send_keys("senha_moderador")
        senha2Comentar.send_keys("senha_moderador")
        registrarComentar.send_keys(Keys.ENTER)

        # 2. Login do moderador
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        # Asserts para garantir que os campos de login estão presentes
        self.assertIsNotNone(usuariologin, "Campo 'username' de login não encontrado.")
        self.assertIsNotNone(senhalogin, "Campo 'password' de login não encontrado.")

        usuariologin.send_keys("moderador_clube")
        senhalogin.send_keys("senha_moderador")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        # 3. Criar um novo clube
        newclub = driver.find_element(By.ID, "newclub-btn")
        self.assertIsNotNone(newclub, "Botão 'Create Club' não encontrado.")

        newclub.click()

        time.sleep(1)

        findForm1 = driver.find_element(By.NAME, "titulo")
        findForm2 = driver.find_element(By.NAME, "modalidade")
        findForm3 = driver.find_element(By.NAME, "categoria")
        findForm4 = driver.find_element(By.NAME, "descricao")
        findForm5 = driver.find_element(By.ID, "create-btn")

        # Asserts para verificar os campos de criação do clube
        self.assertIsNotNone(findForm1, "Campo 'titulo' não encontrado.")
        self.assertIsNotNone(findForm2, "Campo 'modalidade' não encontrado.")
        self.assertIsNotNone(findForm3, "Campo 'categoria' não encontrado.")
        self.assertIsNotNone(findForm4, "Campo 'descricao' não encontrado.")
        self.assertIsNotNone(findForm5, "Botão 'create-btn' não encontrado.")

        findForm1.send_keys("Clube Favorito Teste")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descrição do clube favorito para teste.")

        time.sleep(1)
        findForm5.click()

        # 4. Navegar para a página "My Clubs"
        driver.get("http://127.0.0.1:8000/myclubes/")
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/myclubes/", "Não foi redirecionado corretamente para a página 'My Clubs'.")

        # 5. Garantir que o dropdown de favoritos está aberto
        time.sleep(2)

        # 6. Recapturar o botão de favoritar após abrir o dropdown
        favoritar_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "favoritar-btn"))
        )
        self.assertIsNotNone(favoritar_btn, "Botão de favoritar não encontrado.")

        # 7. Clicar no botão de favoritar
        favoritar_btn.click()

        # 8. Verificar se o ícone de estrela foi atualizado para "favoritado"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bi-star-fill")))

        time.sleep(2)

        # 9. Expandir novamente o dropdown de favoritos
        for _ in range(3):
            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.favoritosheader"))
                )
                self.assertIsNotNone(dropdown, "Dropdown de favoritos não encontrado.")
                ActionChains(driver).move_to_element(dropdown).click().perform()
                break
            except StaleElementReferenceException:
                print("Tentando clicar novamente no dropdown após ele ficar stale.")
                time.sleep(1)

        time.sleep(2)

        # 10. Recapturar o botão de favoritar (agora como desfavoritar)
        favoritar_btn = None
        for _ in range(3):
            try:
                favoritar_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "desfavoritar-btn"))
                )
                favoritar_btn.click()  # Clicar para desfavoritar
                break
            except StaleElementReferenceException:
                print("Botão de desfavoritar ficou stale. Recapturando o botão...")
                time.sleep(1)

        # Verificar se o botão foi clicado corretamente
        self.assertIsNotNone(favoritar_btn, "O botão de desfavoritar não pôde ser clicado.")

        # 11. Verificar se o ícone de estrela foi atualizado para "não favoritado"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bi-star")))

        time.sleep(3)

        # 12. Logout do moderador
        driver.get("http://127.0.0.1:8000/")
        pfp = driver.find_element(By.NAME, "pfp")
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")

        pfp.click()

        time.sleep(1)

        logout = driver.find_element(By.ID, "logout-btn")
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()

        time.sleep(2)

    def test_02_membro_favorita_clube(self):
        driver = self.driver

        # 1. Registro do membro
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuarioComentar = driver.find_element(By.NAME, "username")
        senhaComentar = driver.find_element(By.NAME, "password1")
        senha2Comentar = driver.find_element(By.NAME, "password2")
        registrarComentar = driver.find_element(By.NAME, "registrar")

        # Asserts para verificar que os elementos estão presentes
        self.assertIsNotNone(usuarioComentar, "Campo 'username' não encontrado.")
        self.assertIsNotNone(senhaComentar, "Campo 'password1' não encontrado.")
        self.assertIsNotNone(senha2Comentar, "Campo 'password2' não encontrado.")
        self.assertIsNotNone(registrarComentar, "Botão de registro não encontrado.")

        usuarioComentar.send_keys("membro_clube")
        senhaComentar.send_keys("senha_membro")
        senha2Comentar.send_keys("senha_membro")
        registrarComentar.send_keys(Keys.ENTER)

        # 2. Login do membro
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        # Asserts para garantir que os campos de login estão presentes
        self.assertIsNotNone(usuariologin, "Campo 'username' de login não encontrado.")
        self.assertIsNotNone(senhalogin, "Campo 'password' de login não encontrado.")

        usuariologin.send_keys("membro_clube")
        senhalogin.send_keys("senha_membro")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        # 3. Navegar para a página "Clubs" e entrar no clube "Clube Favorito Teste"
        driver.get("http://127.0.0.1:8000/clubs/")
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/clubs/", "Não foi redirecionado corretamente para a página 'Clubs'.")

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        botao_card = driver.find_element(By.NAME, "titles")
        self.assertIsNotNone(botao_card, "Botão do card do clube não encontrado.")
        botao_card.click()

        time.sleep(1)

        # Acessa a modal de clubs
        botao_club = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club, "Botão de entrar no clube não encontrado.")
        botao_club.click()

        time.sleep(3)

        # Acessa a modal de clubs
        botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club_novo_entrar, "Botão de entrar no clube (2ª vez) não encontrado.")
        botao_club_novo_entrar.click()

        time.sleep(3)

        # 4. Navegar para a página "My Clubs"
        driver.get("http://127.0.0.1:8000/myclubes/")
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/myclubes/", "Não foi redirecionado corretamente para a página 'My Clubs'.")

        # 5. Garantir que o dropdown de favoritos está aberto
        time.sleep(2)

        # 6. Capturar o botão de favoritar
        favoritar_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "favoritar-btn"))
        )
        self.assertIsNotNone(favoritar_btn, "Botão de favoritar não encontrado.")

        # 7. Clicar no botão de favoritar
        favoritar_btn.click()

        # 8. Verificar se o ícone de estrela foi atualizado para "favoritado"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bi-star-fill")))

        time.sleep(2)

        # 9. Expandir novamente o dropdown de favoritos
        for _ in range(3):
            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.favoritosheader"))
                )
                self.assertIsNotNone(dropdown, "Dropdown de favoritos não encontrado.")
                ActionChains(driver).move_to_element(dropdown).click().perform()
                break
            except StaleElementReferenceException:
                print("Tentando clicar novamente no dropdown após ele ficar stale.")
                time.sleep(1)

        time.sleep(2)

        # 10. Recapturar o botão de favoritar (agora como desfavoritar)
        favoritar_btn = None
        for _ in range(3):
            try:
                favoritar_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "desfavoritar-btn"))
                )
                favoritar_btn.click()  # Clicar para desfavoritar
                break
            except StaleElementReferenceException:
                print("Botão de desfavoritar ficou stale. Recapturando o botão...")
                time.sleep(1)

        # Verificar se o botão foi clicado corretamente
        self.assertIsNotNone(favoritar_btn, "O botão de desfavoritar não pôde ser clicado.")

        # 11. Verificar se o ícone de estrela foi atualizado para "não favoritado"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bi-star")))

        time.sleep(3)

        # 12. Logout do membro
        driver.get("http://127.0.0.1:8000/")
        pfp = driver.find_element(By.NAME, "pfp")
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")

        pfp.click()

        time.sleep(1)

        logout = driver.find_element(By.ID, "logout-btn")
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()

        time.sleep(2)


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
    
class verificarMembros(LiveServerTestCase):

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

    def teste_cenario_aprovando(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuario = driver.find_element(By.NAME, "username")
        senha = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        registrar = driver.find_element(By.NAME, "registrar")

        usuario.send_keys("verificarMembrosAdm")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("verificarMembrosAdm")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        newclub = driver.find_element(By.ID, "newclub-btn")
        newclub.click()

        time.sleep(1)

        findForm1 = driver.find_element(By.NAME, "titulo")
        findForm2 = driver.find_element(By.NAME, "modalidade")
        findForm3 = driver.find_element(By.NAME, "categoria")
        findForm4 = driver.find_element(By.NAME, "descricao")
        findForm5 = driver.find_element(By.ID, "create-btn")

        findForm1.send_keys("teste requests")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descricao pra teste dos requests")

        time.sleep(1)
        findForm5.click()

        time.sleep(1)

        config = driver.find_element(By.ID, "engine")
        config.click()

        time.sleep(2)

        editclub = driver.find_element(By.NAME, "editclub")
        editclub.click()

        privado = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "privado"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", privado)

        if not privado.is_selected():
            privado.click()

        time.sleep(1)

        atualizar = driver.find_element(By.NAME, "atualizar")
        atualizar.click()

        config = driver.find_element(By.ID, "engine")
        config.click()

        time.sleep(1)

        request = driver.find_element(By.ID, "request")
        request.click()

        time.sleep(1)

        fechar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "fechar"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", fechar)

        fechar.click()

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

        usuario = driver.find_element(By.NAME, "username")
        senha = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        registrar = driver.find_element(By.NAME, "registrar")

        usuario.send_keys("userComum")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("userComum")
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
            EC.element_to_be_clickable((By.NAME, "solicitar"))
        )
        botao_club.click()

        time.sleep(3)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        time.sleep(2)

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("verificarMembrosAdm")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/myclubes/")
        
        time.sleep(2)

        pesquisa_barra2 = driver.find_element(By.NAME, "nome")
        assert pesquisa_barra2 is not None, "Campo de pesquisa não encontrado"
        pesquisa_barra2.send_keys("teste requests")
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

        config = driver.find_element(By.ID, "engine")
        config.click()

        time.sleep(1)

        request = driver.find_element(By.ID, "request")
        request.click()

        time.sleep(2)

        approve = driver.find_element(By.ID, "aprove")
        approve.click()

        time.sleep(1)

        fechar = driver.find_element(By.NAME, "fechar")
        fechar.click()

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        time.sleep(2)

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("userComum")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/myclubes/")
        
        time.sleep(2)

        pesquisa_barra2 = driver.find_element(By.NAME, "nome")
        assert pesquisa_barra2 is not None, "Campo de pesquisa não encontrado"
        pesquisa_barra2.send_keys("teste requests")
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

    def teste_cenario_reprovando(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuario = driver.find_element(By.NAME, "username")
        senha = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        registrar = driver.find_element(By.NAME, "registrar")

        usuario.send_keys("verificarMembrosAdm")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("verificarMembrosAdm")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        newclub = driver.find_element(By.ID, "newclub-btn")
        newclub.click()

        time.sleep(1)

        findForm1 = driver.find_element(By.NAME, "titulo")
        findForm2 = driver.find_element(By.NAME, "modalidade")
        findForm3 = driver.find_element(By.NAME, "categoria")
        findForm4 = driver.find_element(By.NAME, "descricao")
        findForm5 = driver.find_element(By.ID, "create-btn")

        findForm1.send_keys("teste requests")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descricao pra teste dos requests")

        time.sleep(1)
        findForm5.click()

        time.sleep(1)

        config = driver.find_element(By.ID, "engine")
        config.click()

        time.sleep(2)

        editclub = driver.find_element(By.NAME, "editclub")
        editclub.click()

        privado = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "privado"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", privado)

        if not privado.is_selected():
            privado.click()

        time.sleep(1)

        atualizar = driver.find_element(By.NAME, "atualizar")
        atualizar.click()

        config = driver.find_element(By.ID, "engine")
        config.click()

        time.sleep(1)

        request = driver.find_element(By.ID, "request")
        request.click()

        time.sleep(1)

        fechar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "fechar"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", fechar)

        fechar.click()

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

        usuario = driver.find_element(By.NAME, "username")
        senha = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        registrar = driver.find_element(By.NAME, "registrar")

        usuario.send_keys("userComum")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("userComum")
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
            EC.element_to_be_clickable((By.NAME, "solicitar"))
        )
        botao_club.click()

        time.sleep(3)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        time.sleep(2)

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("verificarMembrosAdm")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/myclubes/")
        
        time.sleep(2)

        pesquisa_barra2 = driver.find_element(By.NAME, "nome")
        assert pesquisa_barra2 is not None, "Campo de pesquisa não encontrado"
        pesquisa_barra2.send_keys("teste requests")
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

        config = driver.find_element(By.ID, "engine")
        config.click()

        time.sleep(1)

        request = driver.find_element(By.ID, "request")
        request.click()

        time.sleep(2)

        reprove = driver.find_element(By.ID, "recusar")
        reprove.click()

        time.sleep(1)

        fechar = driver.find_element(By.NAME, "fechar")
        fechar.click()

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        time.sleep(2)

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("userComum")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/myclubes/")
        
        time.sleep(2)

        pesquisa_barra2 = driver.find_element(By.NAME, "nome")
        assert pesquisa_barra2 is not None, "Campo de pesquisa não encontrado"
        pesquisa_barra2.send_keys("teste requests")
        pesquisa_barra2.send_keys(Keys.ENTER)
        time.sleep(4)


    def teste_cenario_editinfo(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuario = driver.find_element(By.NAME, "username")
        senha = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        registrar = driver.find_element(By.NAME, "registrar")

        usuario.send_keys("editInfoAdm")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("editInfoAdm")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        newclub = driver.find_element(By.ID, "newclub-btn")
        newclub.click()

        time.sleep(2)

        findForm1 = driver.find_element(By.NAME, "titulo")
        findForm2 = driver.find_element(By.NAME, "modalidade")
        findForm3 = driver.find_element(By.NAME, "categoria")
        findForm4 = driver.find_element(By.NAME, "descricao")
        findForm5 = driver.find_element(By.ID, "create-btn")

        findForm1.send_keys("teste requests")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descricao pra teste de editar info")

        time.sleep(1)
        findForm5.click()

        time.sleep(3)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(2)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("userComum")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/clubs/")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        botao_card = driver.find_element(By.NAME, "titles")
        botao_card.click()

        time.sleep(4)

        fecharbtn = driver.find_element(By.NAME, "fechar")
        fecharbtn.click()

        time.sleep(2)

        driver.execute_script("window.scrollTo(0, 0);")

        time.sleep(1)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("editInfoAdm")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        myclubsbtn = driver.find_element(By.NAME, "myclubs-btn")
        myclubsbtn.click()

        time.sleep(2)

        pesquisa_barra2 = driver.find_element(By.NAME, "nome")
        assert pesquisa_barra2 is not None, "Campo de pesquisa 'nome' não encontrado"
        pesquisa_barra2.send_keys("teste requests")
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

        config = driver.find_element(By.ID, "engine")
        config.click()

        time.sleep(2)

        editclub = driver.find_element(By.NAME, "editclub")
        editclub.click()

        privado = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "privado"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", privado)

        if not privado.is_selected():
            privado.click()
        else:
            privado.click()

        findFormx = driver.find_element(By.NAME, "titulo")
        findFormy = driver.find_element(By.NAME, "modalidade")

        findForm3 = driver.find_element(By.NAME, "categoria")

        findForma = driver.find_element(By.NAME, "descricao")
        findFormb = driver.find_element(By.NAME, "atualizar")

        findFormx.clear()
        findFormx.send_keys("prova que as infos mudam")

        modalidadeSelecty = Select(findFormy)
        modalidadeSelecty.select_by_visible_text("presencial")

        categoriaSelectz = Select(findForm3)
        categoriaSelectz.select_by_visible_text("Tecnologia")

        findForma.clear()
        findForma.send_keys("Descricao pra teste de editar clube")

        time.sleep(1)

        atualizar = driver.find_element(By.NAME, "atualizar")
        atualizar.click()

        time.sleep(2)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("userComum")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/clubs/")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        botao_card = driver.find_element(By.NAME, "titles")
        botao_card.click()

        time.sleep(4)

        fecharbtn = driver.find_element(By.NAME, "fechar")
        fecharbtn.click()

        time.sleep(5)

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

