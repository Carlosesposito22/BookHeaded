
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class ProfileViewTest(TestCase):


    def setUp(self):
        # Criar dois usuários e seus perfis
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')


        # Criação de perfis com ícones
        self.profile1 = Profile.objects.create(user=self.user1, bio="Bio do user1", icone="images/icon1.svg")
        self.profile2 = Profile.objects.create(user=self.user2, bio="Bio do user2", icone="images/icon2.svg")


        # Fazer com que user1 siga user2
        self.profile1.seguidores.add(self.user2)


    def test_profile_link_in_navbar(self):
        """Verificar se o link 'Profile' aparece na navbar para usuários logados"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))


        # Verificar se o perfil do usuário está disponível na navbar
        self.assertContains(response, 'Profile')
        self.assertEqual(response.status_code, 200)


    def test_profile_information_display(self):
        """Verificar se as informações do perfil são exibidas corretamente"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user1.id}))


        # Verificar se o nome de usuário, bio, ícone e contagem de seguidores/seguidos são exibidos
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
