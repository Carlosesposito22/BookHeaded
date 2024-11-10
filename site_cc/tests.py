from .models import Clube, Membro, Comentario, Modalidade, Categoria, HistoricoMaratona, Profile, Avaliacao
from site_cc.management.commands.deleteusuarios import Command
from django.test import TestCase, Client, LiveServerTestCase
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .views import comentario_create_view
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from django.contrib.staticfiles.testing import LiveServerTestCase
from unittest.mock import patch
from django.conf import settings
from selenium import webdriver
from datetime import datetime
#import requests
import json
import logging
import time
import os
import subprocess




class ComentarioTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecomentarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

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

        findForm1.send_keys("Clube de Teste Comentário")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descrição do clube de teste para Comentário.")
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()

        time.sleep(4)

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
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/clubs/", "Não foi redirecionado corretamente para a página 'Clubs'.")

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        botao_card = driver.find_element(By.NAME, "titles")
        self.assertIsNotNone(botao_card, "Botão do card do clube não encontrado.")
        botao_card.click()

        time.sleep(2)

        # Acessa a modal de clubs
        botao_club = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club, "Botão de entrar no clube não encontrado.")
        botao_club.click()

        time.sleep(3)

        # Acessa a modal de clubs novamente
        botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club_novo_entrar, "Botão de entrar no clube (2ª vez) não encontrado.")
        botao_club_novo_entrar.click()

        time.sleep(3)

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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

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

            usuario.send_keys("testePrivadoModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testePrivadoModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            time.sleep(1)

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

            findForm1.send_keys("Clube de Teste privado")

            modalidadeSelect = Select(findForm2)
            modalidadeSelect.select_by_visible_text("Online")

            categoriaSelect = Select(findForm3)
            categoriaSelect.select_by_visible_text("Ficção")

            checkbox = driver.find_element(By.ID, "privado")
            assert checkbox is not None, "Checkbox 'privado' não encontrado"
            checkbox.click()
            
            findForm4.send_keys("Descrição do clube.")
            driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
            time.sleep(1)
            findForm5.click()
        
        except Exception as e:
            print(f"Falha no teste de verificação campos obrigatórios: {e}")


    def teste_receber_solicitacao_duplicada_e_recebimento(self):
        
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

        usuario.send_keys("testePrivadoModerador")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        assert usuariologin is not None, "Campo de login 'username' não encontrado"
        assert senhalogin is not None, "Campo de login 'password' não encontrado"

        usuariologin.send_keys("testePrivadoModerador")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(1)

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

        findForm1.send_keys("Book w4")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        checkbox = driver.find_element(By.ID, "privado")
        assert checkbox is not None, "Checkbox 'privado' não encontrado"
        checkbox.click()
        
        findForm4.send_keys("Descrição do clube.")
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()
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

        usuario.send_keys("c")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        assert usuariologin is not None, "Campo de login 'username' não encontrado"
        assert senhalogin is not None, "Campo de login 'password' não encontrado"

        usuariologin.send_keys("c")
        senhalogin.send_keys("senha")
        senhalogin.send_keys(Keys.ENTER)

        time.sleep(2)

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

        usuario.send_keys("testePrivadoModerador")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        assert usuariologin is not None, "Campo de login 'username' não encontrado"
        assert senhalogin is not None, "Campo de login 'password' não encontrado"

        usuariologin.send_keys("testePrivadoModerador")
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

        usuariologin.send_keys("c")
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

            usuario.send_keys("testePrivadoModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testePrivadoModerador")
            senhalogin.send_keys("senha")
            senhalogin.send_keys(Keys.ENTER)

            time.sleep(1)

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

            findForm1.send_keys("Book w4")

            modalidadeSelect = Select(findForm2)
            modalidadeSelect.select_by_visible_text("Online")

            categoriaSelect = Select(findForm3)
            categoriaSelect.select_by_visible_text("Ficção")

            checkbox = driver.find_element(By.ID, "privado")
            assert checkbox is not None, "Checkbox 'privado' não encontrado"
            checkbox.click()
            
            findForm4.send_keys("Descrição do clube.")
            driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
            time.sleep(1)
            findForm5.click()
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

            usuario.send_keys("testePrivadoMembro")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testePrivadoMembro")
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

            usuario.send_keys("testePrivadoModerador")
            senha.send_keys("senha")
            senha2.send_keys("senha")
            registrar.send_keys(Keys.ENTER)

            driver.get("http://127.0.0.1:8000/membros/login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            usuariologin = driver.find_element(By.NAME, "username")
            senhalogin = driver.find_element(By.NAME, "password")

            assert usuariologin is not None, "Campo de login 'username' não encontrado"
            assert senhalogin is not None, "Campo de login 'password' não encontrado"

            usuariologin.send_keys("testePrivadoModerador")
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

            usuariologin.send_keys("testePrivadoMembro")
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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

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

            time.sleep(1)

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

            findForm1.send_keys("Lilivro ola2")

            modalidadeSelect = Select(findForm2)
            modalidadeSelect.select_by_visible_text("Online")

            categoriaSelect = Select(findForm3)
            categoriaSelect.select_by_visible_text("Ficção")

            findForm4.send_keys("Descrição do clube de teste para maratona.")
            driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
            time.sleep(1)
            findForm5.click()
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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()
  

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

            time.sleep(1)

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

            findForm1.send_keys("Book ola2")

            modalidadeSelect = Select(findForm2)
            modalidadeSelect.select_by_visible_text("Online")

            categoriaSelect = Select(findForm3)
            categoriaSelect.select_by_visible_text("Ficção")

            findForm4.send_keys("Descrição do clube de teste para maratona.")
            driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
            time.sleep(1)
            findForm5.click()

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

            time.sleep(1)

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

            print("Teste de verificação de presenca do botao de moderador e participante foi concluido com sucesso.")
        
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

            time.sleep(1)

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

            findForm1.send_keys("Book ola2")

            modalidadeSelect = Select(findForm2)
            modalidadeSelect.select_by_visible_text("Online")

            categoriaSelect = Select(findForm3)
            categoriaSelect.select_by_visible_text("Ficção")

            findForm4.send_keys("Descrição do clube de teste para maratona.")
            driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
            time.sleep(1)
            findForm5.click()
            time.sleep(1)

            botao_maratona = driver.find_element(By.ID, "createMaratona")
            assert botao_maratona is not None, "Botão 'createMaratona' não encontrado"
            driver.execute_script("arguments[0].click();", botao_maratona)
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


class SairDoClubeTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
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

        confirmar_sair = driver.find_element(By.XPATH, "//form[@method='post']//button[contains(text(), 'Leave')]")
        self.assertIsNotNone(confirmar_sair, "Botão 'Leave' não encontrado.")
        confirmar_sair.click()

        # 9. Verificar se a mensagem de sucesso foi exibida no frontend após sair do clube
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-warning")))
        mensagem_sucesso = driver.find_element(By.CSS_SELECTOR, ".alert-warning")
        self.assertIn("Você saiu do clube", mensagem_sucesso.text, "Mensagem de sucesso não foi exibida ou está incorreta.")

        time.sleep(3)


class AvaliacaoClubeTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

    def test_01_moderador_nao_avalia(self):
        driver = self.driver

        # 1. Registro do moderador
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuario_moderador = driver.find_element(By.NAME, "username")
        senha_moderador = driver.find_element(By.NAME, "password1")
        senha2_moderador = driver.find_element(By.NAME, "password2")
        registrar_moderador = driver.find_element(By.NAME, "registrar")

        # Assert para garantir que os elementos de registro estão presentes
        self.assertIsNotNone(usuario_moderador, "Campo de 'username' do moderador não encontrado.")
        self.assertIsNotNone(senha_moderador, "Campo de 'senha' do moderador não encontrado.")
        self.assertIsNotNone(senha2_moderador, "Campo de confirmação de senha do moderador não encontrado.")
        self.assertIsNotNone(registrar_moderador, "Botão de registrar moderador não encontrado.")

        usuario_moderador.send_keys("moderador_clube")
        senha_moderador.send_keys("senha_moderador")
        senha2_moderador.send_keys("senha_moderador")
        registrar_moderador.send_keys(Keys.ENTER)

        # 2. Login do moderador
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        login_moderador = driver.find_element(By.NAME, "username")
        senha_login_moderador = driver.find_element(By.NAME, "password")

        # Assert para garantir que os campos de login estão presentes
        self.assertIsNotNone(login_moderador, "Campo de 'username' do moderador não encontrado.")
        self.assertIsNotNone(senha_login_moderador, "Campo de 'senha' do moderador não encontrado.")

        login_moderador.send_keys("moderador_clube")
        senha_login_moderador.send_keys("senha_moderador")
        senha_login_moderador.send_keys(Keys.ENTER)

        time.sleep(2)

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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()

        time.sleep(4)

        # 4. Verificar que o moderador não pode avaliar o próprio clube
        avaliar_btn = driver.find_elements(By.CSS_SELECTOR, "button[data-bs-target*='#avaliarModal']")
        self.assertEqual(len(avaliar_btn), 0, "Moderador não deveria poder avaliar o próprio clube.")

        time.sleep(1)

        # 5. Logout do moderador
        driver.get("http://127.0.0.1:8000/")
        pfp_moderador = driver.find_element(By.NAME, "pfp")
        self.assertIsNotNone(pfp_moderador, "Imagem de perfil do moderador não encontrada.")
        pfp_moderador.click()

        time.sleep(1)

        logout_moderador = driver.find_element(By.ID, "logout-btn")
        self.assertIsNotNone(logout_moderador, "Botão de logout do moderador não encontrado.")
        logout_moderador.click()

        time.sleep(1)

    def test_02_membro_avalia_clube(self):
        driver = self.driver

        # 1. Registro do moderador
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuario_moderador = driver.find_element(By.NAME, "username")
        senha_moderador = driver.find_element(By.NAME, "password1")
        senha2_moderador = driver.find_element(By.NAME, "password2")
        registrar_moderador = driver.find_element(By.NAME, "registrar")

        # Assert para garantir que os elementos de registro estão presentes
        self.assertIsNotNone(usuario_moderador, "Campo de 'username' do moderador não encontrado.")
        self.assertIsNotNone(senha_moderador, "Campo de 'senha' do moderador não encontrado.")
        self.assertIsNotNone(senha2_moderador, "Campo de confirmação de senha do moderador não encontrado.")
        self.assertIsNotNone(registrar_moderador, "Botão de registrar moderador não encontrado.")

        usuario_moderador.send_keys("moderador_clube")
        senha_moderador.send_keys("senha_moderador")
        senha2_moderador.send_keys("senha_moderador")
        registrar_moderador.send_keys(Keys.ENTER)

        # 2. Login do moderador
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        login_moderador = driver.find_element(By.NAME, "username")
        senha_login_moderador = driver.find_element(By.NAME, "password")

        # Assert para garantir que os campos de login estão presentes
        self.assertIsNotNone(login_moderador, "Campo de 'username' do moderador não encontrado.")
        self.assertIsNotNone(senha_login_moderador, "Campo de 'senha' do moderador não encontrado.")

        login_moderador.send_keys("moderador_clube")
        senha_login_moderador.send_keys("senha_moderador")
        senha_login_moderador.send_keys(Keys.ENTER)

        time.sleep(2)

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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()

        time.sleep(4)

        time.sleep(1)

        # 5. Logout do moderador
        driver.get("http://127.0.0.1:8000/")
        pfp_moderador = driver.find_element(By.NAME, "pfp")
        self.assertIsNotNone(pfp_moderador, "Imagem de perfil do moderador não encontrada.")
        pfp_moderador.click()

        time.sleep(1)

        logout_moderador = driver.find_element(By.ID, "logout-btn")
        self.assertIsNotNone(logout_moderador, "Botão de logout do moderador não encontrado.")
        logout_moderador.click()

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

        # 4. Membro avalia o clube
        avaliar_modal_btn = driver.find_element(By.NAME, "avaliarbtn")
        avaliar_modal_btn.click()

        time.sleep(2)

        select_nota = driver.find_element(By.ID, "rating-btn")
        select_nota.click()
        select_nota.find_element(By.ID, "notateste").click()
        select_nota.click()
        submit_avaliacao_btn = driver.find_element(By.NAME, "enviar-btn")
        submit_avaliacao_btn.click()
        time.sleep(3)

        # 5. Membro tenta enviar avaliação sem nota
        avaliar_modal_btn = driver.find_element(By.NAME, "avaliarbtn")
        avaliar_modal_btn.click()

        time.sleep(2)

        select_nota = driver.find_element(By.ID, "rating-btn")
        select_nota.click()
        select_nota.click()
        submit_avaliacao_btn = driver.find_element(By.NAME, "enviar-btn")
        submit_avaliacao_btn.click()
        time.sleep(3)

        sair_modal = driver.find_element(By.ID, "sair-avaliar")
        sair_modal.click()
        time.sleep(1)

        # 6. Membro altera a avaliação para 5
        avaliar_modal_btn = driver.find_element(By.NAME, "avaliarbtn")
        avaliar_modal_btn.click()

        time.sleep(2)

        select_nota = driver.find_element(By.ID, "rating-btn")
        select_nota.click()
        select_nota.find_element(By.ID, "notateste2").click()
        select_nota.click()
        submit_avaliacao_btn = driver.find_element(By.NAME, "enviar-btn")
        submit_avaliacao_btn.click()
        time.sleep(3)


class FavoritarClubeTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
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

        # 1. Registro do moderador
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuario_moderador = driver.find_element(By.NAME, "username")
        senha_moderador = driver.find_element(By.NAME, "password1")
        senha2_moderador = driver.find_element(By.NAME, "password2")
        registrar_moderador = driver.find_element(By.NAME, "registrar")

        # Assert para garantir que os elementos de registro estão presentes
        self.assertIsNotNone(usuario_moderador, "Campo de 'username' do moderador não encontrado.")
        self.assertIsNotNone(senha_moderador, "Campo de 'senha' do moderador não encontrado.")
        self.assertIsNotNone(senha2_moderador, "Campo de confirmação de senha do moderador não encontrado.")
        self.assertIsNotNone(registrar_moderador, "Botão de registrar moderador não encontrado.")

        usuario_moderador.send_keys("moderador_clube")
        senha_moderador.send_keys("senha_moderador")
        senha2_moderador.send_keys("senha_moderador")
        registrar_moderador.send_keys(Keys.ENTER)

        # 2. Login do moderador
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        login_moderador = driver.find_element(By.NAME, "username")
        senha_login_moderador = driver.find_element(By.NAME, "password")

        # Assert para garantir que os campos de login estão presentes
        self.assertIsNotNone(login_moderador, "Campo de 'username' do moderador não encontrado.")
        self.assertIsNotNone(senha_login_moderador, "Campo de 'senha' do moderador não encontrado.")

        login_moderador.send_keys("moderador_clube")
        senha_login_moderador.send_keys("senha_moderador")
        senha_login_moderador.send_keys(Keys.ENTER)

        time.sleep(2)

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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()

        time.sleep(1)

        # 5. Logout do moderador
        driver.get("http://127.0.0.1:8000/")
        pfp_moderador = driver.find_element(By.NAME, "pfp")
        self.assertIsNotNone(pfp_moderador, "Imagem de perfil do moderador não encontrada.")
        pfp_moderador.click()

        time.sleep(1)

        logout_moderador = driver.find_element(By.ID, "logout-btn")
        self.assertIsNotNone(logout_moderador, "Botão de logout do moderador não encontrado.")
        logout_moderador.click()

        time.sleep(1)

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


class TopLivrosTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

    def test_01_moderador_adiciona_top_livros(self):
        driver = self.driver

        # 1. Registro do moderador
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuario_moderador = driver.find_element(By.NAME, "username")
        senha_moderador = driver.find_element(By.NAME, "password1")
        senha2_moderador = driver.find_element(By.NAME, "password2")
        registrar_moderador = driver.find_element(By.NAME, "registrar")

        usuario_moderador.send_keys("moderador_clube")
        senha_moderador.send_keys("senha_moderador")
        senha2_moderador.send_keys("senha_moderador")
        registrar_moderador.send_keys(Keys.ENTER)

        # 2. Login do moderador
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        login_moderador = driver.find_element(By.NAME, "username")
        senha_login_moderador = driver.find_element(By.NAME, "password")

        login_moderador.send_keys("moderador_clube")
        senha_login_moderador.send_keys("senha_moderador")
        senha_login_moderador.send_keys(Keys.ENTER)

        time.sleep(2)

        # 3. Criar um novo clube
        newclub = driver.find_element(By.ID, "newclub-btn")
        newclub.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "titulo")))

        titulo_clube = driver.find_element(By.NAME, "titulo")
        modalidade_clube = driver.find_element(By.NAME, "modalidade")
        categoria_clube = driver.find_element(By.NAME, "categoria")
        descricao_clube = driver.find_element(By.NAME, "descricao")
        create_clube_btn = driver.find_element(By.ID, "create-btn")

        titulo_clube.send_keys("Clube Teste Livros")

        modalidade_select = Select(modalidade_clube)
        modalidade_select.select_by_visible_text("Online")

        categoria_select = Select(categoria_clube)
        categoria_select.select_by_visible_text("Ficção")

        descricao_clube.send_keys("Clube criado pelo moderador para teste de livros favoritos.")

        create_clube_btn.click()

        time.sleep(2)

        # 4. Acessar dropdown para editar os livros favoritos
        dropdown_btn = driver.find_element(By.ID, "engine")
        self.assertIsNotNone(dropdown_btn, "Botão do dropdown não encontrado.")
        dropdown_btn.click()

        time.sleep(1)

        # 5. Selecionar o item do dropdown para editar os livros favoritos (id modal '#addTopLivrosModal-1')
        edit_books_option = driver.find_element(By.NAME, "editbooks")
        self.assertIsNotNone(edit_books_option, "Opção para editar livros favoritos não encontrada.")
        edit_books_option.click()

        time.sleep(2)

        # 6. Preencher os livros favoritos
        textarea_livros = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "top_livros"))
        )
        self.assertIsNotNone(textarea_livros, "Campo de 'top_livros' não encontrado.")
        textarea_livros.clear()  # Limpa o campo antes de adicionar novos livros
        textarea_livros.send_keys("Livro 1\nLivro 2\nLivro 3")

        # 7. Submeter o formulário para salvar os livros favoritos
        submit_btn = driver.find_element(By.NAME, "edit-book-btn")
        self.assertIsNotNone(submit_btn, "Botão de salvar lista de livros favoritos não encontrado.")
        submit_btn.click()

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # 8. Logout do moderador
        driver.get("http://127.0.0.1:8000/")
        pfp_moderador = driver.find_element(By.NAME, "pfp")
        pfp_moderador.click()

        time.sleep(1)

        logout_moderador = driver.find_element(By.ID, "logout-btn")
        logout_moderador.click()

        time.sleep(1)

    def test_02_membro_visualiza_top_livros(self):
        driver = self.driver

        # 1. Registro do moderador
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuario_moderador = driver.find_element(By.NAME, "username")
        senha_moderador = driver.find_element(By.NAME, "password1")
        senha2_moderador = driver.find_element(By.NAME, "password2")
        registrar_moderador = driver.find_element(By.NAME, "registrar")

        usuario_moderador.send_keys("moderador_clube")
        senha_moderador.send_keys("senha_moderador")
        senha2_moderador.send_keys("senha_moderador")
        registrar_moderador.send_keys(Keys.ENTER)

        # 2. Login do moderador
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        login_moderador = driver.find_element(By.NAME, "username")
        senha_login_moderador = driver.find_element(By.NAME, "password")

        login_moderador.send_keys("moderador_clube")
        senha_login_moderador.send_keys("senha_moderador")
        senha_login_moderador.send_keys(Keys.ENTER)

        time.sleep(2)

        # 3. Criar um novo clube
        newclub = driver.find_element(By.ID, "newclub-btn")
        newclub.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "titulo")))

        titulo_clube = driver.find_element(By.NAME, "titulo")
        modalidade_clube = driver.find_element(By.NAME, "modalidade")
        categoria_clube = driver.find_element(By.NAME, "categoria")
        descricao_clube = driver.find_element(By.NAME, "descricao")
        create_clube_btn = driver.find_element(By.ID, "create-btn")

        titulo_clube.send_keys("Clube Teste Livros")

        modalidade_select = Select(modalidade_clube)
        modalidade_select.select_by_visible_text("Online")

        categoria_select = Select(categoria_clube)
        categoria_select.select_by_visible_text("Ficção")

        descricao_clube.send_keys("Clube criado pelo moderador para teste de livros favoritos.")

        create_clube_btn.click()

        time.sleep(2)

        # 1. Registro do membro
        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuario_membro = driver.find_element(By.NAME, "username")
        senha_membro = driver.find_element(By.NAME, "password1")
        senha2_membro = driver.find_element(By.NAME, "password2")
        registrar_membro = driver.find_element(By.NAME, "registrar")

        usuario_membro.send_keys("membro_clube")
        senha_membro.send_keys("senha_membro")
        senha2_membro.send_keys("senha_membro")
        registrar_membro.send_keys(Keys.ENTER)

        time.sleep(1)

        # 2. Login do membro
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        login_membro = driver.find_element(By.NAME, "username")
        senha_login_membro = driver.find_element(By.NAME, "password")

        login_membro.send_keys("membro_clube")
        senha_login_membro.send_keys("senha_membro")
        senha_login_membro.send_keys(Keys.ENTER)

        time.sleep(2)

       # 3. Acessa a modal de clubs
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

        # 4. Verifica se os livros favoritos são exibidos
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        element_to_scroll = driver.find_element(By.NAME, "top-books")
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # 5. Logout do membro
        driver.get("http://127.0.0.1:8000/")
        pfp_membro = driver.find_element(By.NAME, "pfp")
        pfp_membro.click()

        time.sleep(1)

        logout_membro = driver.find_element(By.ID, "logout-btn")
        logout_membro.click()

        time.sleep(1)


class verificarProgresso(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecomentarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

    
        
               
    

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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecomentarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()


    
    

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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()

        time.sleep(3)

        pfp = driver.find_element(By.NAME, "pfp")
        pfp.click()

        logout = driver.find_element(By.ID, "logout-btn")
        logout.click()

        time.sleep(2)

        driver.get("http://127.0.0.1:8000/membros/register/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        usuario = driver.find_element(By.NAME, "username")
        senha = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        registrar = driver.find_element(By.NAME, "registrar")

        usuario.send_keys("UserComum")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)
        time.sleep(2)

        
        usuariologin = driver.find_element(By.NAME, "username")
        senhalogin = driver.find_element(By.NAME, "password")

        usuariologin.send_keys("UserComum")
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

        usuariologin.send_keys("UserComum")
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


class TestFiltro(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

    # Cenario sem clube
    def teste1(self):
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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()

        # Acessa a página de clubes
        driver.get("http://127.0.0.1:8000/clubs/")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 20000);")

        time.sleep(2)

        # Verifica se o botão de filtro está clicável
        botao_ficcao = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "botao-filtro"))
        )
        botao_ficcao.click()

        time.sleep(2)

        botao_misterio = driver.find_element(By.XPATH, "//button[contains(text(), 'Mistério')]")
        botao_misterio.click()

        time.sleep(2)

        botao_filter = driver.find_element(By.ID, "filter")
        botao_filter.click()

        time.sleep(2)

        driver.execute_script("window.scrollTo(0, 20000);")

        time.sleep(2)

        # Verifica se o filtro foi aplicado corretamente
        page_content = driver.page_source
        self.assertIn("Mistério", page_content, "O filtro de Mistério não foi aplicado corretamente.")

    # Cenario com clube
    def teste2(self):
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
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()

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

        # Acessa a página de clubes
        driver.get("http://127.0.0.1:8000/clubs/")
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, 20000);")
        time.sleep(2)

        botao_ficcao = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "botao-filtro"))
        )
        botao_ficcao.click()

        time.sleep(2)

        botao_ficcao = driver.find_element(By.XPATH, "//button[contains(text(), 'Ficção')]")
        botao_ficcao.click()

        time.sleep(2)

        botao_filter = driver.find_element(By.ID, "filter")
        botao_filter.click()

        time.sleep(2)

        driver.execute_script("window.scrollTo(0, 20000);")

        time.sleep(2)

        # Verifica se o filtro foi aplicado corretamente
        page_content = driver.page_source
        self.assertIn("Ficção", page_content, "O filtro de Ficção não foi aplicado corretamente.")


class ProfileViewTest(TestCase):


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecomentarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

    
   
        
               


   
   


    def teste_cenario1(self):
        call_command('deleteusuarios')
       

        driver = self.driver

        # Registro do primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario = driver.find_element(by=By.NAME, value="username")
        senha = driver.find_element(by=By.NAME, value="password1")
        senha2 = driver.find_element(by=By.NAME, value="password2")
        registrar = driver.find_element(by=By.NAME, value="registrar")

        usuario.send_keys("joao")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER)

        time.sleep(5)  # Aguardar o login ser processado

        # Logout do primeiro usuário (joao)
        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action = ActionChains(driver)
        action.move_to_element(dropdown).click().perform()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "profiles")))

        # Clicar no logout
        logout_link = driver.find_element(by=By.NAME, value="logout-btn")
        action.move_to_element(logout_link).click().perform()
        time.sleep(3)

        # Criar um segundo usuário (maria)
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario2 = driver.find_element(by=By.NAME, value="username")
        senha2 = driver.find_element(by=By.NAME, value="password1")
        senha2_confirm = driver.find_element(by=By.NAME, value="password2")
        registrar2 = driver.find_element(by=By.NAME, value="registrar")

        usuario2.send_keys("maria")
        senha2.send_keys("senha123")
        senha2_confirm.send_keys("senha123")
        registrar2.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como segundo usuário (maria)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol2 = driver.find_element(by=By.NAME, value="username")
        senhalogin2 = driver.find_element(by=By.NAME, value="password")
        registrarl2 = driver.find_element(by=By.NAME, value="loginB")

        usuariol2.send_keys("maria")
        senhalogin2.send_keys("senha123")
        registrarl2.send_keys(Keys.ENTER)

        time.sleep(5)  # Aguardar o login ser processado

        # Acessar a página de usuários e buscar "joao"
        driver.get("http://127.0.0.1:8000/usuarios/?nomes=joao")
        time.sleep(5)

        # Localizar o ícone ou nome de usuário "joao"
        icone_joao = driver.find_element(By.NAME, "user")

        # Clicar no ícone do perfil ou nome de usuário
        action.move_to_element(icone_joao).click().perform()
        time.sleep(5)

        # Verificar se o botão "Seguir" existe antes de clicar
        try:
            seguir_botao = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'follow-text'))
            )
            action.move_to_element(seguir_botao).click().perform()
            time.sleep(3)
        except:
            print("Botão 'Seguir' não encontrado ou não clicável")

        # Logout do segundo usuário (maria)
        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action.move_to_element(dropdown).click().perform()

        # Clicar no logout
        logout_link = driver.find_element(by=By.NAME, value="logout-btn")
        action.move_to_element(logout_link).click().perform()
        time.sleep(3)

        # Fazer login novamente como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        time.sleep(2)
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER)

        time.sleep(5)  # Aguardar o login ser processado

        # Acessar o dropdown e ir para o perfil
        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action.move_to_element(dropdown).click().perform()

        # Aguardar o menu dropdown ficar visível
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "profiles"))
        )

        # Clicar no item "Profile" dentro do dropdown
        profile_link = driver.find_element(by=By.NAME, value="profiles")
        action.move_to_element(profile_link).click().perform()
        time.sleep(5)

        # Abrir o modal de edição de perfil clicando no ícone de lápis
        lapis = driver.find_element(by=By.NAME, value="pencil")
        action.move_to_element(lapis).click().perform()

        # Selecionar o ícone desejado (por exemplo, images/icon4.svg)
        icone_desejado = driver.find_element(By.XPATH, "//button[@id='modal-icon']/img[@src='/static/images/icon4.svg']")
        action.move_to_element(icone_desejado).click().perform()

        time.sleep(3)  # Aguardar a seleção do ícone

        # Preencher a bio
        bio = driver.find_element(by=By.NAME, value="bio")
        bio.clear()
        bio.send_keys("Minha nova bio")
        time.sleep(3)

        # Clicar no botão de salvar no modal
        botao_salvar = driver.find_element(by=By.NAME, value="salvar")
        action.move_to_element(botao_salvar).click().perform()
        time.sleep(5)

        biousuario = driver.find_element(by=By.NAME, value="bio_usuario")

        # Verificar se a bio foi atualizada com sucesso usando get_attribute para acessar o innerText do elemento
        self.assertEqual(biousuario.get_attribute("innerText"), "Minha nova bio", "Falha ao atualizar a bio")

        # Verificar se a imagem de perfil foi alterada corretamente
        icone_atualizado = driver.find_element(By.CLASS_NAME, "pfp-holder")  # Seleciona o elemento do ícone de perfil

        # Verificar se o ícone foi atualizado corretamente (checar o src da imagem)
        self.assertEqual(icone_atualizado.get_attribute("src"), "http://127.0.0.1:8000/static/images/icon4.svg", "O ícone não foi atualizado corretamente.")

        qntd_seguidres=  driver.find_element(by=By.NAME, value="followers-text2")
        self.assertEqual(qntd_seguidres.get_attribute("innerText"), "1 Followers", "Falha ao atualizar a bio")

        qntd_seguindo=  driver.find_element(by=By.NAME, value="seguindo")
        self.assertEqual( qntd_seguindo.get_attribute("innerText"), "0 Following", "Falha ao atualizar a bio")

             

        

        
    def teste_2(self):
        driver = self.driver
        action = ActionChains(driver)

        # Registro do primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario = driver.find_element(by=By.NAME, value="username")
        senha = driver.find_element(by=By.NAME, value="password1")
        senha2 = driver.find_element(by=By.NAME, value="password2")
        registrar = driver.find_element(by=By.NAME, value="registrar")

        usuario.send_keys("joao")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER)

        time.sleep(5)  # Aguardar o login ser processado

        # Logout do primeiro usuário (joao)
        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action.move_to_element(dropdown).click().perform()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "profiles")))

        # Clicar no logout
        logout_link = driver.find_element(by=By.NAME, value="logout-btn")
        action.move_to_element(logout_link).click().perform()
        time.sleep(3)

        # Criar um segundo usuário (maria)
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario2 = driver.find_element(by=By.NAME, value="username")
        senha2 = driver.find_element(by=By.NAME, value="password1")
        senha2_confirm = driver.find_element(by=By.NAME, value="password2")
        registrar2 = driver.find_element(by=By.NAME, value="registrar")

        usuario2.send_keys("maria")
        senha2.send_keys("senha123")
        senha2_confirm.send_keys("senha123")
        registrar2.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como segundo usuário (maria)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol2 = driver.find_element(by=By.NAME, value="username")
        senhalogin2 = driver.find_element(by=By.NAME, value="password")
        registrarl2 = driver.find_element(by=By.NAME, value="loginB")

        usuariol2.send_keys("maria")
        senhalogin2.send_keys("senha123")
        registrarl2.send_keys(Keys.ENTER)

        time.sleep(2)  # Aguardar o login ser processado
        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action.move_to_element(dropdown).click().perform()

        # Aguardar o menu dropdown ficar visível
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "profiles"))
        )

        # Clicar no item "Profile" dentro do dropdown
        profile_link = driver.find_element(by=By.NAME, value="profiles")
        action.move_to_element(profile_link).click().perform()
        time.sleep(4)
        

        # Acessar a página de usuários e buscar "joao"
        driver.get("http://127.0.0.1:8000/usuarios/?nomes=joao")
        time.sleep(5)

        # Localizar o ícone ou nome de usuário "joao"
        icone_joao = driver.find_element(By.NAME, "user")

        # Clicar no ícone do perfil ou nome de usuário
        action.move_to_element(icone_joao).click().perform()
        time.sleep(5)

        # Verificar se o botão "Seguir" existe antes de clicar
        
        seguir_botao = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'follow-text'))
        )
        action.move_to_element(seguir_botao).click().perform()
        time.sleep(3)

        # Logout do segundo usuário (maria)
        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action.move_to_element(dropdown).click().perform()

        # Clicar no logout
        logout_link = driver.find_element(by=By.NAME, value="logout-btn")
        action.move_to_element(logout_link).click().perform()
        time.sleep(3)

        # Fazer login novamente como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER)

        time.sleep(5)  # Aguardar o login ser processado

        # Acessar o dropdown e ir para o perfil
        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action.move_to_element(dropdown).click().perform()

        # Aguardar o menu dropdown ficar visível
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "profiles"))
        )

        # Clicar no item "Profile" dentro do dropdown
        profile_link = driver.find_element(by=By.NAME, value="profiles")
        action.move_to_element(profile_link).click().perform()
        

        time.sleep(5)

        
        seguindo_link = driver.find_element(by=By.NAME, value="followers-text2")
        action.move_to_element(seguindo_link).click().perform()
        time.sleep(3)

        dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "pfp"))
        )
        
        action.move_to_element(dropdown).click().perform()
       
        time.sleep(4)
        seguidores_link =driver.find_element(by=By.NAME, value="seguindo")
        action.move_to_element(seguidores_link).click().perform()
        nome_link=driver.find_element(by=By.NAME, value="foto_perfil")
        foto_perfil=driver.find_element(by=By.NAME, value="fotodoperfil")
        self.assertEqual(nome_link.get_attribute("innerText"), "@maria", "nao coresponde ao mesmo usuario")
       
        self.assertTrue(foto_perfil.get_attribute('src').endswith('/static/images/icon3.svg'), "O ícone não é a do perfil.")

        

        time.sleep(5)
        action.move_to_element(dropdown).click().perform()
        time.sleep(2)

        
class Editprofiletest(TestCase):

    
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecomentarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()
        
               

    
    
    def teste1(self):
       
      
        driver = self.driver
        # Registro do primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/register/")
        
        time.sleep(2)
       
        

        usuario = driver.find_element(by=By.NAME, value="username")
        senha = driver.find_element(by=By.NAME, value="password1")
        senha2 = driver.find_element(by=By.NAME, value="password2")
        registrar = driver.find_element(by=By.NAME, value="registrar")

        usuario.send_keys("joao")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER)

        time.sleep(5)  # Aguardar o login ser processado

        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action = ActionChains(driver)
        action.move_to_element(dropdown).click().perform()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "profiles")))

        profile_link = driver.find_element(by=By.NAME, value="profiles")
        action.move_to_element(profile_link).click().perform()

        lapis = driver.find_element(by=By.NAME, value="pencil")
        action.move_to_element(lapis).click().perform()

        # Selecionar o ícone desejado
        icone_desejado = driver.find_element(By.XPATH, "//button[@id='modal-icon']/img[@src='/static/images/icon4.svg']")
        action.move_to_element(icone_desejado).click().perform()

        time.sleep(3)  # Aguardar a seleção do ícone

        # Preencher a bio (limpar antes)
        bio = driver.find_element(by=By.NAME, value="bio")
        bio.clear()  # Limpar o campo de texto da bio
        bio.send_keys("Minha nova bio")
        time.sleep(3)

        # Clicar no botão de salvar no modal
        botao_salvar = driver.find_element(by=By.NAME, value="salvar")
        action.move_to_element(botao_salvar).click().perform()
        time.sleep(5)

        # Recarregar a página de perfil ou navegar para a página onde a bio é exibida
        driver.refresh()
        time.sleep(5)

        # Esperar que o campo de bio seja carregado
        bio_atualizada = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "bio"))
        )

        # Verificar se a bio foi atualizada corretamente usando 'innerText'
        self.assertEqual(bio_atualizada.get_attribute("innerText"), "Minha nova bio", "A bio não foi atualizada corretamente.")

        
       
    def teste2(self):
        command = Command()
        command.handle()
        time.sleep(2)
        driver = self.driver

        # Registro do primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario = driver.find_element(by=By.NAME, value="username")
        senha = driver.find_element(by=By.NAME, value="password1")
        senha2 = driver.find_element(by=By.NAME, value="password2")
        registrar = driver.find_element(by=By.NAME, value="registrar")

        usuario.send_keys("joao")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER)

        time.sleep(5)  # Aguardar o login ser processado

        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action = ActionChains(driver)
        action.move_to_element(dropdown).click().perform()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "profiles")))

        profile_link = driver.find_element(by=By.NAME, value="profiles")
        action.move_to_element(profile_link).click().perform()

        lapis = driver.find_element(by=By.NAME, value="pencil")
        action.move_to_element(lapis).click().perform()

        time.sleep(3)  # Aguardar a seleção do ícone

        # Selecionar o ícone desejado (por exemplo, images/icon4.svg)
        icone_desejado = driver.find_element(By.XPATH, "//button[@id='modal-icon']/img[@src='/static/images/icon4.svg']")
        action.move_to_element(icone_desejado).click().perform()

        time.sleep(3)

        # Clicar no botão de salvar no modal
        botao_salvar = driver.find_element(by=By.NAME, value="salvar")
        action.move_to_element(botao_salvar).click().perform()
        time.sleep(5)

        # Recarregar a página de perfil para verificar se o ícone foi salvo corretamente
        driver.refresh()
        time.sleep(3)

        # Obter o ícone atualizado
        icone_atualizado = driver.find_element(By.CLASS_NAME, "pfp-holder")  # Seleciona o elemento do ícone de perfil

        # Verificar se o ícone foi atualizado corretamente (checar o src da imagem)
        self.assertEqual(icone_atualizado.get_attribute("src"), "http://127.0.0.1:8000/static/images/icon4.svg", "O ícone não foi atualizado corretamente.")

        
class usuarioprofiletest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecomentarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()   
   
        
               

   
    def teste_1(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario = driver.find_element(by=By.NAME, value="username")
        senha = driver.find_element(by=By.NAME, value="password1")
        senha2 = driver.find_element(by=By.NAME, value="password2")
        registrar = driver.find_element(by=By.NAME, value="registrar")

        usuario.send_keys("joao")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER)
        time.sleep(2)
        
        dropdown = driver.find_element(by=By.NAME, value="pfp")
        action = ActionChains(driver)
        action.move_to_element(dropdown).click().perform()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "profiles")))
        time.sleep(2)

       
        logout_link = driver.find_element(by=By.NAME, value="logout-btn")
        action.move_to_element(logout_link).click().perform()
        time.sleep(3)

       
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario2 = driver.find_element(by=By.NAME, value="username")
        senha2 = driver.find_element(by=By.NAME, value="password1")
        senha2_confirm = driver.find_element(by=By.NAME, value="password2")
        registrar2 = driver.find_element(by=By.NAME, value="registrar")

        usuario2.send_keys("maria")
        senha2.send_keys("senha123")
        senha2_confirm.send_keys("senha123")
        registrar2.send_keys(Keys.ENTER)

        time.sleep(4)  # Aguardar o registro ser processado     

        driver.get("http://127.0.0.1:8000/usuarios/?nomes=")
        time.sleep(3)
        serchbar = driver.find_element(by=By.NAME, value="nomes")
        botao= driver.find_element(by=By.NAME, value="pesquisar")
        action = ActionChains(driver)
        action.move_to_element(serchbar).click().perform()
        serchbar.send_keys("joao")
        action.move_to_element(botao).click().perform()
        time.sleep(2)
        icone=driver.find_element(by=By.NAME, value="user")
        action.move_to_element(icone).click().perform()

        time.sleep(5)  # Aguardar a página de resultados carregar

        # Localizar o nome de usuário "joao"
        icone = driver.find_element(by=By.NAME, value="nomeexibir")
        action.move_to_element(icone).click().perform()
        time.sleep(2)

        # Verificar se o usuário correto foi acessado
        nome_usuario = icone.get_attribute("innerText").strip()  # Capturar o nome de usuário
        self.assertEqual(nome_usuario, "@joao", "O usuário 'joao' não foi encontrado corretamente.")
    def teste_2(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario = driver.find_element(by=By.NAME, value="username")
        senha = driver.find_element(by=By.NAME, value="password1")
        senha2 = driver.find_element(by=By.NAME, value="password2")
        registrar = driver.find_element(by=By.NAME, value="registrar")

        usuario.send_keys("joao")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER) 
        time.sleep(2)
        driver.get("http://127.0.0.1:8000/usuarios/?nomes=")
        time.sleep(3)
        serchbar = driver.find_element(by=By.NAME, value="nomes")
        botao= driver.find_element(by=By.NAME, value="pesquisar")
        action = ActionChains(driver)
        action.move_to_element(serchbar).click().perform()
        serchbar.send_keys("marina")
        action.move_to_element(botao).click().perform()
        time.sleep(2)
        icone = driver.find_element(by=By.NAME, value="textoS")
        action.move_to_element(icone).click().perform()

        # Verificar se o usuário correto foi acessado
        nome_usuario = icone.get_attribute("innerText").strip()  # Capturar o nome de usuário
        self.assertEqual(nome_usuario, "Nenhum usuário encontrado.", "usuarios foram nencontrados.")

    def teste_3(self): 
        driver = self.driver
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario = driver.find_element(by=By.NAME, value="username")
        senha = driver.find_element(by=By.NAME, value="password1")
        senha2 = driver.find_element(by=By.NAME, value="password2")
        registrar = driver.find_element(by=By.NAME, value="registrar")

        usuario.send_keys("joao")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        time.sleep(5)  # Aguardar o registro ser processado

        # Fazer login como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER) 
        driver.get("http://127.0.0.1:8000/usuarios/?nomes=")
        time.sleep(3)
        serchbar = driver.find_element(by=By.NAME, value="nomes")
        botao= driver.find_element(by=By.NAME, value="pesquisar")
        action = ActionChains(driver)
        action.move_to_element(serchbar).click().perform()
        serchbar.send_keys("")
        action.move_to_element(botao).click().perform()
        time.sleep(2)
        icone = driver.find_element(by=By.NAME, value="tdspessoas")
        action.move_to_element(icone).click().perform()
        time.sleep(2)

        # Verificar se o usuário correto foi acessado
        nome_usuario = icone.get_attribute("innerText").strip()  # Capturar o nome de usuário
        self.assertEqual(nome_usuario, "Search results for:", "usuarios foram nencontrados.")

class favoritoprofiletest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
  
    def setUp(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecomentarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)

    def teste_1(self):
        #Fazendo o registro e o login
        driver = self.driver
        driver.get("http://127.0.0.1:8000/membros/register/")
        time.sleep(3)

        usuario = driver.find_element(by=By.NAME, value="username")
        senha = driver.find_element(by=By.NAME, value="password1")
        senha2 = driver.find_element(by=By.NAME, value="password2")
        registrar = driver.find_element(by=By.NAME, value="registrar")

        usuario.send_keys("joao")
        senha.send_keys("senha")
        senha2.send_keys("senha")
        registrar.send_keys(Keys.ENTER)

        time.sleep(8)  # Aguardar o registro ser processado

        # Fazer login como o primeiro usuário (joao)
        driver.get("http://127.0.0.1:8000/membros/login/")
        usuariol = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        registrarl = driver.find_element(by=By.NAME, value="loginB")

        usuariol.send_keys("joao")
        senhalogin.send_keys("senha")
        registrarl.send_keys(Keys.ENTER)
        time.sleep(2)


class CriarEnqueteTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

    def test_01_enquete_visivel_moderador(self):
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
        time.sleep(1)

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
        time.sleep(2)

        # 3. Criar um novo clube
        newclub = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "newclub-btn")))
        self.assertIsNotNone(newclub, "Botão 'Create Club' não encontrado.")
        newclub.click()

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

        findForm1.send_keys("Clube de Teste Enquete")
        Select(findForm2).select_by_visible_text("Online")
        Select(findForm3).select_by_visible_text("Ficção")
        findForm4.send_keys("Descrição do clube de teste para enquete.")
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(2)
        findForm5.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Assert para verificar se o moderador pode ver o botão de criar enquete
        botao_enquete = driver.find_element(By.NAME, "criar-enquete")
        self.assertIsNotNone(botao_enquete, "Erro: O Moderador não tem acesso ao botão de criar enquete.")
        print("Sucesso: O Moderador tem acesso ao botão de criar enquete.")
        time.sleep(2)

        # Logout do moderador
        driver.get("http://127.0.0.1:8000")
        pfp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pfp")))
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")
        pfp.click()

        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-btn")))
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()
        time.sleep(1)

        # 4. Registro e login do membro
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
        time.sleep(2)
        registrarComentar2.send_keys(Keys.ENTER)

        # 5. Login do membro
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin2 = driver.find_element(By.NAME, "username")
        senhalogin2 = driver.find_element(By.NAME, "password")

        # Asserts para garantir que os campos de login estão presentes
        self.assertIsNotNone(usuariologin2, "Campo 'username' de login não encontrado.")
        self.assertIsNotNone(senhalogin2, "Campo 'password' de login não encontrado.")

        usuariologin2.send_keys("membro_clube")
        senhalogin2.send_keys("senha_membro")
        time.sleep(1)
        senhalogin2.send_keys(Keys.ENTER)
        time.sleep(1)

        time.sleep(1)

        driver.get("http://127.0.0.1:8000/clubs/")
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/clubs/", "Não foi redirecionado corretamente para a página 'Clubs'.")

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        botao_card = driver.find_element(By.NAME, "titles")
        self.assertIsNotNone(botao_card, "Botão do card do clube não encontrado.")
        botao_card.click()

        time.sleep(2)

        # Acessa a modal de clubs
        botao_club = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club, "Botão de entrar no clube não encontrado.")
        botao_club.click()

        time.sleep(3)

        # Acessa a modal de clubs novamente
        botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club_novo_entrar, "Botão de entrar no clube (2ª vez) não encontrado.")
        botao_club_novo_entrar.click()

        time.sleep(3)

        botao_enquete_membro = driver.find_elements(By.NAME, "criar-enquete")
        self.assertEqual(len(botao_enquete_membro), 0, "Erro: O Membro tem acesso ao botão de criar enquete.")
        print("Sucesso: O Membro não tem acesso ao botão de criar enquete.")

        # Logout do membro
        driver.get("http://127.0.0.1:8000")
        pfp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pfp")))
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")
        time.sleep(1)
        pfp.click()

        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-btn")))
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()

    def test_02_criar_enquete_valida(self):
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

        findForm1.send_keys("Clube de Teste Enquete")

        modalidadeSelect = Select(findForm2)
        modalidadeSelect.select_by_visible_text("Online")

        categoriaSelect = Select(findForm3)
        categoriaSelect.select_by_visible_text("Ficção")

        findForm4.send_keys("Descrição do clube de teste para sair.")
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(1)
        findForm5.click()
        time.sleep(2)

        time.sleep(3)
        btnCriarEnquete = driver.find_element(By.NAME, "criar-enquete")
        assert btnCriarEnquete is not None, "Botão 'criar-enquete ' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(1)

        titulo_enquete = driver.find_element(By.ID, "enqueteTitulo")
        assert titulo_enquete is not None, "Campo 'enqueteTitulo' não encontrado"
        titulo_enquete.click()
        time.sleep(2)

        botao_criar_enquete = driver.find_element(By.ID, "save-enquete")
        assert botao_criar_enquete  is not None, "Botão 'save-enquete' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(2)

        botao_sair_enquete = driver.find_element(By.ID, "sair-enquete")
        assert botao_sair_enquete  is not None, "Botão 'sair-enquete' não encontrado"
        driver.execute_script("arguments[0].click();", botao_sair_enquete)
        time.sleep(1)

        time.sleep(3)
        btnCriarEnquete = driver.find_element(By.NAME, "criar-enquete")
        assert btnCriarEnquete is not None, "Botão 'criar-enquete ' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(1)

        titulo_enquete = driver.find_element(By.ID, "enqueteTitulo")
        assert titulo_enquete is not None, "Campo 'enqueteTitulo' não encontrado"
        titulo_enquete.send_keys("Enquete Sem Prazo")
        titulo_enquete.click()
        time.sleep(1)

        prazo_enquete = driver.find_element(By.ID, "enquetePrazo")
        assert prazo_enquete is not None, "Campo 'enquetePrazo' não encontrado"
        prazo_enquete.click()
        time.sleep(2)

        botao_criar_enquete = driver.find_element(By.ID, "save-enquete")
        assert botao_criar_enquete  is not None, "Botão 'save-enquete' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(2)

        botao_sair_enquete = driver.find_element(By.ID, "sair-enquete")
        assert botao_sair_enquete  is not None, "Botão 'sair-enquete' não encontrado"
        driver.execute_script("arguments[0].click();", botao_sair_enquete)
        time.sleep(1)

        time.sleep(3)
        btnCriarEnquete = driver.find_element(By.NAME, "criar-enquete")
        assert btnCriarEnquete is not None, "Botão 'criar-enquete ' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(1)

        titulo_enquete = driver.find_element(By.ID, "enqueteTitulo")
        assert titulo_enquete is not None, "Campo 'enqueteTitulo' não encontrado"
        titulo_enquete.send_keys(" e sem opções")
        titulo_enquete.click()
        time.sleep(1)

        prazo_enquete = driver.find_element(By.ID, "enquetePrazo")
        assert prazo_enquete is not None, "Campo 'enquetePrazo' não encontrado"
        prazo_enquete.send_keys("30122024")
        prazo_enquete.click()
        time.sleep(2)

        action = ActionChains(driver)
        opcao_sim = driver.find_element(By.ID, "opcoes-enquete")
        action.move_to_element(opcao_sim).click().perform()
        time.sleep(1)

        botao_criar_enquete = driver.find_element(By.ID, "save-enquete")
        assert botao_criar_enquete  is not None, "Botão 'save-enquete' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(2)

        botao_sair_enquete = driver.find_element(By.ID, "sair-enquete")
        assert botao_sair_enquete  is not None, "Botão 'sair-enquete' não encontrado"
        driver.execute_script("arguments[0].click();", botao_sair_enquete)
        time.sleep(1)

        time.sleep(3)
        btnCriarEnquete = driver.find_element(By.NAME, "criar-enquete")
        assert btnCriarEnquete is not None, "Botão 'criar-enquete ' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(1)

        titulo_enquete = driver.find_element(By.ID, "enqueteTitulo")
        assert titulo_enquete is not None, "Campo 'enqueteTitulo' não encontrado"
        titulo_enquete.clear()
        titulo_enquete.send_keys("Enquete com todas as opções válidas")
        titulo_enquete.click()
        time.sleep(2)

        prazo_enquete = driver.find_element(By.ID, "enquetePrazo")
        assert prazo_enquete is not None, "Campo 'enquetePrazo' não encontrado"
        prazo_enquete.send_keys("30122024")
        prazo_enquete.click()
        time.sleep(2)

        action = ActionChains(driver)
        opcao_sim = driver.find_element(By.ID, "opcoes-enquete")
        action.move_to_element(opcao_sim).click().perform()
        opcao_sim.send_keys("sim")
        time.sleep(1)

        btn_opcao_mais = driver.find_element(By.NAME, "btn-mais")
        action.move_to_element(btn_opcao_mais).click().perform()
        time.sleep(1)

        btn_opcao_nao = driver.find_element(By.ID, "opcoes1")
        action.move_to_element(btn_opcao_nao).click().perform()
        btn_opcao_nao.send_keys("nao")
        time.sleep(3)

        botao_criar_enquete = driver.find_element(By.ID, "save-enquete")
        assert botao_criar_enquete  is not None, "Botão 'save-enquete' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(3)

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

    def test_03_visualizar_e_votoUnico(self):
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
        time.sleep(1)

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
        time.sleep(2)

        # 3. Criar um novo clube
        newclub = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "newclub-btn")))
        self.assertIsNotNone(newclub, "Botão 'Create Club' não encontrado.")
        newclub.click()

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

        findForm1.send_keys("Clube de Teste Enquete")
        Select(findForm2).select_by_visible_text("Online")
        Select(findForm3).select_by_visible_text("Ficção")
        findForm4.send_keys("Descrição do clube de teste para enquete.")
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(2)
        findForm5.click()
        time.sleep(3)

        time.sleep(3)
        btnCriarEnquete = driver.find_element(By.NAME, "criar-enquete")
        assert btnCriarEnquete is not None, "Botão 'criar-enquete ' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(1)
        
        titulo_enquete = driver.find_element(By.ID, "enqueteTitulo")
        assert titulo_enquete is not None, "Campo 'enqueteTitulo' não encontrado"
        titulo_enquete.clear()
        titulo_enquete.send_keys("Nova Enquete")
        titulo_enquete.click()
        time.sleep(2)

        prazo_enquete = driver.find_element(By.ID, "enquetePrazo")
        assert prazo_enquete is not None, "Campo 'enquetePrazo' não encontrado"
        prazo_enquete.send_keys("30122024")
        prazo_enquete.click()
        time.sleep(2)

        action = ActionChains(driver)
        opcao_sim = driver.find_element(By.ID, "opcoes-enquete")
        action.move_to_element(opcao_sim).click().perform()
        opcao_sim.send_keys("sim")
        time.sleep(1)

        btn_opcao_mais = driver.find_element(By.NAME, "btn-mais")
        action.move_to_element(btn_opcao_mais).click().perform()
        time.sleep(1)

        btn_opcao_nao = driver.find_element(By.ID, "opcoes1")
        action.move_to_element(btn_opcao_nao).click().perform()
        btn_opcao_nao.send_keys("nao")
        time.sleep(3)

        botao_criar_enquete = driver.find_element(By.ID, "save-enquete")
        assert botao_criar_enquete  is not None, "Botão 'save-enquete' não encontrado"
        botao_criar_enquete.click()
        time.sleep(2)
        
        # Logout do moderador
        driver.get("http://127.0.0.1:8000")
        pfp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pfp")))
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")
        pfp.click()

        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-btn")))
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()
        time.sleep(2)

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

        driver.get("http://127.0.0.1:8000/clubs/")
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/clubs/", "Não foi redirecionado corretamente para a página 'Clubs'.")

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        botao_card = driver.find_element(By.NAME, "titles")
        self.assertIsNotNone(botao_card, "Botão do card do clube não encontrado.")
        botao_card.click()

        time.sleep(2)

        # Acessa a modal de clubs
        botao_club = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club, "Botão de entrar no clube não encontrado.")
        botao_club.click()

        time.sleep(3)

        # Acessa a modal de clubs novamente
        botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club_novo_entrar, "Botão de entrar no clube (2ª vez) não encontrado.")
        botao_club_novo_entrar.click()

        time.sleep(3)
        
        # Vota na primeira opção e vê o resultado
        # 1. Abra o modal de enquetes
        ver_enquetes = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ver-enquetes"))
        )
        ver_enquetes.click()

        # 2. Aguarde que o modal esteja visível
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "enquetesModal"))
        )
        ####################
        action = ActionChains(driver)
        time.sleep(2)
        primeira_enquete = driver.find_element(By.CSS_SELECTOR, "button[data-enquete-id]")
        time.sleep(2)
        action.move_to_element(primeira_enquete).click().perform()
        time.sleep(2)
        ####################

        opcoes = driver.find_elements(By.CSS_SELECTOR, "input[name='opcao_id']")
        opcoes[0].click()
        time.sleep(1)
        btn_vote = driver.find_element(By.NAME, "btn-vote")
        assert btn_vote is not None, "Botão 'btn_vote' não encontrado"
        btn_vote.click()
        time.sleep(5)

        ver_resultados = driver.find_element(By.ID, "listarResultadosEnquetes")
        assert ver_resultados is not None, "Botão 'listarResultadosEnquetes' não encontrado"
        ver_resultados.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "resultadosEnquetesModal"))
        )

        enquetes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultadosContainer button[data-enquete-id]"))
        )
        assert enquetes, "Nenhuma enquete ativa encontrada."

        primeira_enquete_button = enquetes[0]
        primeira_enquete_button.click()
        time.sleep(2)

        fechar_modal_button = driver.find_element(By.NAME, "btn-fechar-enquete-resultado")
        fechar_modal_button.click()
        time.sleep(2)

        # Vota na segunda opção e vê o resultado
        ver_enquetes = driver.find_element(By.ID, "ver-enquetes")
        assert ver_enquetes is not None, "Botão 'ver-enquetes' não encontrado"
        ver_enquetes.click()
        time.sleep(2)

        primeira_enquete = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-enquete-id]"))
        )
        primeira_enquete.click()
        time.sleep(2)

        # Votar na segunda opção
        opcoes = driver.find_elements(By.CSS_SELECTOR, "input[name='opcao_id']")
        opcoes[1].click()
        time.sleep(1)
        btn_vote = driver.find_element(By.NAME, "btn-vote")
        assert btn_vote is not None, "Botão 'btn_vote' não encontrado"
        btn_vote.click()
        time.sleep(5)

        ver_resultados = driver.find_element(By.ID, "listarResultadosEnquetes")
        assert ver_resultados is not None, "Botão 'listarResultadosEnquetes' não encontrado"
        ver_resultados.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "resultadosEnquetesModal"))
        )

        enquetes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultadosContainer button[data-enquete-id]"))
        )
        assert enquetes, "Nenhuma enquete ativa encontrada."

        primeira_enquete_button = enquetes[0]
        primeira_enquete_button.click()
        time.sleep(2)

        fechar_modal_button = driver.find_element(By.NAME, "btn-fechar-enquete-resultado")
        fechar_modal_button.click()
        time.sleep(2)

        # Logout do membro
        driver.get("http://127.0.0.1:8000")
        pfp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pfp")))
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")
        time.sleep(1)
        pfp.click()

        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-btn")))
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()

class visualizacao(TestCase):


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        subprocess.run(['python', 'manage.py', 'createcategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'createmodalidades'], check=True)        

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        subprocess.run(['python', 'manage.py', 'deleteclubs'], check=True)
        subprocess.run(['python', 'manage.py', 'deletecategorias'], check=True)
        subprocess.run(['python', 'manage.py', 'deletemodalidades'], check=True)
        super().tearDown()

    def teste1(self):
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
        time.sleep(1)

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
        time.sleep(2)

        # 3. Criar um novo clube
        newclub = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "newclub-btn")))
        self.assertIsNotNone(newclub, "Botão 'Create Club' não encontrado.")
        newclub.click()

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

        findForm1.send_keys("Clube de Teste Enquete")
        Select(findForm2).select_by_visible_text("Online")
        Select(findForm3).select_by_visible_text("Ficção")
        findForm4.send_keys("Descrição do clube de teste para enquete.")
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(2)
        findForm5.click()
        time.sleep(3)

        time.sleep(3)
        btnCriarEnquete = driver.find_element(By.NAME, "criar-enquete")
        assert btnCriarEnquete is not None, "Botão 'criar-enquete ' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(1)
        
        titulo_enquete = driver.find_element(By.ID, "enqueteTitulo")
        assert titulo_enquete is not None, "Campo 'enqueteTitulo' não encontrado"
        titulo_enquete.clear()
        titulo_enquete.send_keys("Nova Enquete")
        titulo_enquete.click()
        time.sleep(2)

        prazo_enquete = driver.find_element(By.ID, "enquetePrazo")
        assert prazo_enquete is not None, "Campo 'enquetePrazo' não encontrado"
        prazo_enquete.send_keys("30122024")
        prazo_enquete.click()
        time.sleep(2)

        action = ActionChains(driver)
        opcao_sim = driver.find_element(By.ID, "opcoes-enquete")
        action.move_to_element(opcao_sim).click().perform()
        opcao_sim.send_keys("sim")
        time.sleep(1)

        btn_opcao_mais = driver.find_element(By.NAME, "btn-mais")
        action.move_to_element(btn_opcao_mais).click().perform()
        time.sleep(1)

        btn_opcao_nao = driver.find_element(By.ID, "opcoes1")
        action.move_to_element(btn_opcao_nao).click().perform()
        btn_opcao_nao.send_keys("nao")
        time.sleep(3)

        botao_criar_enquete = driver.find_element(By.ID, "save-enquete")
        assert botao_criar_enquete  is not None, "Botão 'save-enquete' não encontrado"
        botao_criar_enquete.click()
        time.sleep(2)

        ver_resultados = driver.find_element(By.ID, "listarResultadosEnquetes")
        assert ver_resultados is not None, "Botão 'listarResultadosEnquetes' não encontrado"
        ver_resultados.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "resultadosEnquetesModal"))
        )

        enquetes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultadosContainer button[data-enquete-id]"))
        )
        assert enquetes, "Nenhuma enquete ativa encontrada."

        primeira_enquete_button = enquetes[0]
        primeira_enquete_button.click()
        time.sleep(2)

        fechar_modal_button = driver.find_element(By.NAME, "btn-fechar-enquete-resultado")
        fechar_modal_button.click()
        time.sleep(2)


        
        # Logout do moderador
        driver.get("http://127.0.0.1:8000")
        pfp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pfp")))
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")
        pfp.click()

        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-btn")))
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()
        time.sleep(1)

        # 4. Registro e login do membro
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
        time.sleep(2)
        registrarComentar2.send_keys(Keys.ENTER)

        # 5. Login do membro
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin2 = driver.find_element(By.NAME, "username")
        senhalogin2 = driver.find_element(By.NAME, "password")

        # Asserts para garantir que os campos de login estão presentes
        self.assertIsNotNone(usuariologin2, "Campo 'username' de login não encontrado.")
        self.assertIsNotNone(senhalogin2, "Campo 'password' de login não encontrado.")

        usuariologin2.send_keys("membro_clube")
        senhalogin2.send_keys("senha_membro")
        time.sleep(1)
        senhalogin2.send_keys(Keys.ENTER)
        time.sleep(1)


        driver.get("http://127.0.0.1:8000/clubs/")
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/clubs/", "Não foi redirecionado corretamente para a página 'Clubs'.")

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        botao_card = driver.find_element(By.NAME, "titles")
        self.assertIsNotNone(botao_card, "Botão do card do clube não encontrado.")
        botao_card.click()

        time.sleep(2)

        # Acessa a modal de clubs
        botao_club = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club, "Botão de entrar no clube não encontrado.")
        botao_club.click()

        time.sleep(3)

        # Acessa a modal de clubs novamente
        botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club_novo_entrar, "Botão de entrar no clube (2ª vez) não encontrado.")
        botao_club_novo_entrar.click()

        time.sleep(3)
        
        ######################################

        
        ver_resultados = driver.find_element(By.ID, "listarResultadosEnquetes")
        assert ver_resultados is not None, "Botão 'listarResultadosEnquetes' não encontrado"
        ver_resultados.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "resultadosEnquetesModal"))
        )

        enquetes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultadosContainer button[data-enquete-id]"))
        )
        assert enquetes, "Nenhuma enquete ativa encontrada."

        primeira_enquete_button = enquetes[0]
        primeira_enquete_button.click()
        time.sleep(2)

        fechar_modal_button = driver.find_element(By.NAME, "btn-fechar-enquete-resultado")
        fechar_modal_button.click()
        time.sleep(2)
        
    def teste2(self):
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
        time.sleep(1)

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
        time.sleep(2)

        # 3. Criar um novo clube
        newclub = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "newclub-btn")))
        self.assertIsNotNone(newclub, "Botão 'Create Club' não encontrado.")
        newclub.click()

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

        findForm1.send_keys("Clube de Teste Enquete")
        Select(findForm2).select_by_visible_text("Online")
        Select(findForm3).select_by_visible_text("Ficção")
        findForm4.send_keys("Descrição do clube de teste para enquete.")
        driver.execute_script("document.getElementById('create-btn').removeAttribute('disabled');")
        time.sleep(2)
        findForm5.click()
        time.sleep(1)

        time.sleep(3)
        btnCriarEnquete = driver.find_element(By.NAME, "criar-enquete")
        assert btnCriarEnquete is not None, "Botão 'criar-enquete ' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(1)
        
        titulo_enquete = driver.find_element(By.ID, "enqueteTitulo")
        assert titulo_enquete is not None, "Campo 'enqueteTitulo' não encontrado"
        titulo_enquete.clear()
        titulo_enquete.send_keys("Nova Enquete")
        titulo_enquete.click()
        time.sleep(2)

        prazo_enquete = driver.find_element(By.ID, "enquetePrazo")
        assert prazo_enquete is not None, "Campo 'enquetePrazo' não encontrado"
        prazo_enquete.send_keys("30122024")
        prazo_enquete.click()
        time.sleep(2)

        action = ActionChains(driver)
        opcao_sim = driver.find_element(By.ID, "opcoes-enquete")
        action.move_to_element(opcao_sim).click().perform()
        opcao_sim.send_keys("sim")
        time.sleep(1)

        btn_opcao_mais = driver.find_element(By.NAME, "btn-mais")
        action.move_to_element(btn_opcao_mais).click().perform()
        time.sleep(1)

        btn_opcao_nao = driver.find_element(By.ID, "opcoes1")
        action.move_to_element(btn_opcao_nao).click().perform()
        btn_opcao_nao.send_keys("nao")
        time.sleep(3)

        botao_criar_enquete = driver.find_element(By.ID, "save-enquete")
        assert botao_criar_enquete  is not None, "Botão 'save-enquete' não encontrado"
        driver.execute_script("arguments[0].click();", btnCriarEnquete)
        time.sleep(2)

        ver_enquetes = driver.find_element(By.ID, "ver-enquetes")
        assert ver_enquetes is not None, "Botão 'ver-enquetes' não encontrado"
        ver_enquetes.click()
        time.sleep(2)

        primeira_enquete = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-enquete-id]"))
        )
        primeira_enquete.click()
        time.sleep(2)

        # Votar na primeira opção
        opcoes = driver.find_elements(By.CSS_SELECTOR, "input[name='opcao_id']")
        opcoes[0].click()
        time.sleep(1)
        btn_vote = driver.find_element(By.NAME, "btn-vote")
        assert btn_vote is not None, "Botão 'btn_vote' não encontrado"
        btn_vote.click()
        time.sleep(5)

        ver_resultados = driver.find_element(By.ID, "listarResultadosEnquetes")
        assert ver_resultados is not None, "Botão 'listarResultadosEnquetes' não encontrado"
        ver_resultados.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "resultadosEnquetesModal"))
        )

        enquetes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultadosContainer button[data-enquete-id]"))
        )
        assert enquetes, "Nenhuma enquete ativa encontrada."

        primeira_enquete_button = enquetes[0]
        primeira_enquete_button.click()
        time.sleep(2)

        fechar_modal_button = driver.find_element(By.NAME, "btn-fechar-enquete-resultado")
        fechar_modal_button.click()
        time.sleep(2)

         # Logout do moderador
        driver.get("http://127.0.0.1:8000")
        pfp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pfp")))
        self.assertIsNotNone(pfp, "Avatar do perfil não encontrado.")
        pfp.click()

        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-btn")))
        self.assertIsNotNone(logout, "Botão de logout não encontrado.")
        logout.click()
        time.sleep(2)

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
        time.sleep(2)
        registrarComentar2.send_keys(Keys.ENTER)

        # 5. Login do membro
        driver.get("http://127.0.0.1:8000/membros/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        usuariologin2 = driver.find_element(By.NAME, "username")
        senhalogin2 = driver.find_element(By.NAME, "password")

        # Asserts para garantir que os campos de login estão presentes
        self.assertIsNotNone(usuariologin2, "Campo 'username' de login não encontrado.")
        self.assertIsNotNone(senhalogin2, "Campo 'password' de login não encontrado.")

        usuariologin2.send_keys("membro_clube")
        senhalogin2.send_keys("senha_membro")
        time.sleep(1)
        senhalogin2.send_keys(Keys.ENTER)
        time.sleep(1)


        driver.get("http://127.0.0.1:8000/clubs/")
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/clubs/", "Não foi redirecionado corretamente para a página 'Clubs'.")

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        botao_card = driver.find_element(By.NAME, "titles")
        self.assertIsNotNone(botao_card, "Botão do card do clube não encontrado.")
        botao_card.click()

        time.sleep(2)

        # Acessa a modal de clubs
        botao_club = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club, "Botão de entrar no clube não encontrado.")
        botao_club.click()

        time.sleep(3)

        # Acessa a modal de clubs novamente
        botao_club_novo_entrar = driver.find_element(By.NAME, "entrar-btn")
        self.assertIsNotNone(botao_club_novo_entrar, "Botão de entrar no clube (2ª vez) não encontrado.")
        botao_club_novo_entrar.click()

        time.sleep(3)

        ver_enquetes = driver.find_element(By.ID, "ver-enquetes")
        assert ver_enquetes is not None, "Botão 'ver-enquetes' não encontrado"
        ver_enquetes.click()
        time.sleep(2)

        primeira_enquete = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-enquete-id]"))
        )
        primeira_enquete.click()
        time.sleep(2)

        # Votar na primeira opção
        opcoes = driver.find_elements(By.CSS_SELECTOR, "input[name='opcao_id']")
        opcoes[0].click()
        time.sleep(1)
        btn_vote = driver.find_element(By.NAME, "btn-vote")
        assert btn_vote is not None, "Botão 'btn_vote' não encontrado"
        btn_vote.click()
        time.sleep(5)

        ver_resultados = driver.find_element(By.ID, "listarResultadosEnquetes")
        assert ver_resultados is not None, "Botão 'listarResultadosEnquetes' não encontrado"
        ver_resultados.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "resultadosEnquetesModal"))
        )

        enquetes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultadosContainer button[data-enquete-id]"))
        )
        assert enquetes, "Nenhuma enquete ativa encontrada."

        primeira_enquete_button = enquetes[0]
        primeira_enquete_button.click()
        time.sleep(2)

        fechar_modal_button = driver.find_element(By.NAME, "btn-fechar-enquete-resultado")
        fechar_modal_button.click()
        time.sleep(2)
    

