from django.contrib.auth.models import User
from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from .models import Clube, Membro, Comentario, Modalidade, Categoria, HistoricoMaratona, Profile, Avaliacao
from .views import comentario_create_view
from unittest.mock import patch
from django.conf import settings
from django.http import HttpResponseForbidden
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import requests
import json
import logging
import time
import os


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