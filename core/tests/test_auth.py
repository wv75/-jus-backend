import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTestCase(TestCase):
    """Testes para autenticação e autorização"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_landing_page_accessible(self):
        """Testa se a landing page é acessível sem login"""
        response = self.client.get(reverse('core:landing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jus-Baía')
    
    def test_login_page_accessible(self):
        """Testa se a página de login é acessível"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Entrar na Plataforma')
    
    def test_login_with_valid_credentials(self):
        """Testa login com credenciais válidas"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Deve redirecionar após login bem-sucedido
        self.assertEqual(response.status_code, 302)
    
    def test_login_with_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Deve retornar à página de login com erro
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_logout_redirects_to_landing(self):
        """Testa se logout redireciona para landing page"""
        # Primeiro faz login
        self.client.login(username='testuser', password='testpass123')
        
        # Depois faz logout
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('core:landing'))
    
    def test_dashboard_requires_login(self):
        """Testa se dashboard requer login"""
        response = self.client.get('/dashboard/')
        # Deve redirecionar para login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_dashboard_accessible_after_login(self):
        """Testa se dashboard é acessível após login"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        # Deve ser acessível (200) ou redirecionar para dashboard específico (302)
        self.assertIn(response.status_code, [200, 302])


class UserCreationTestCase(TestCase):
    """Testes para criação de usuários"""
    
    def test_create_user(self):
        """Testa criação de usuário"""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpass123'
        )
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('newpass123'))
    
    def test_user_string_representation(self):
        """Testa representação string do usuário"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')


@pytest.mark.django_db
class TestAuthenticationPytest:
    """Testes usando pytest para autenticação"""
    
    def test_user_creation_pytest(self):
        """Teste de criação de usuário com pytest"""
        user = User.objects.create_user(
            username='pytestuser',
            email='pytest@example.com',
            password='pytestpass123'
        )
        assert user.username == 'pytestuser'
        assert user.email == 'pytest@example.com'
        assert user.check_password('pytestpass123')
    
    def test_landing_page_pytest(self, client):
        """Teste da landing page com pytest"""
        response = client.get(reverse('core:landing'))
        assert response.status_code == 200
        assert 'Jus-Baía' in response.content.decode()
