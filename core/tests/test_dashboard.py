import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class DashboardRedirectTestCase(TestCase):
    """Testes para redirecionamento do dashboard"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='dashboarduser',
            email='dashboard@example.com',
            password='dashpass123'
        )
    
    def test_dashboard_redirect_without_login(self):
        """Testa se /dashboard/ redireciona para login quando não logado"""
        response = self.client.get('/dashboard/')
        # Deve redirecionar para login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_dashboard_redirect_with_login(self):
        """Testa se /dashboard/ redireciona para /dashboard/executivo/ quando logado"""
        self.client.login(username='dashboarduser', password='dashpass123')
        response = self.client.get('/dashboard/')
        # Deve redirecionar para dashboard executivo
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/executivo/')
    
    def test_dashboard_executivo_accessible_after_login(self):
        """Testa se /dashboard/executivo/ é acessível após login"""
        self.client.login(username='dashboarduser', password='dashpass123')
        response = self.client.get('/dashboard/executivo/')
        # Deve ser acessível (200) ou redirecionar internamente (302)
        self.assertIn(response.status_code, [200, 302])
    
    def test_dashboard_operacional_accessible_after_login(self):
        """Testa se /dashboard/operacional/ é acessível após login"""
        self.client.login(username='dashboarduser', password='dashpass123')
        response = self.client.get('/dashboard/operacional/')
        # Deve ser acessível (200) ou redirecionar internamente (302)
        self.assertIn(response.status_code, [200, 302])


class DatabaseConfigTestCase(TestCase):
    """Testes para verificar configuração do banco de dados"""
    
    def test_database_connection(self):
        """Testa se a conexão com o banco está funcionando"""
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        self.assertEqual(result[0], 1)
    
    def test_user_model_works(self):
        """Testa se o modelo User está funcionando com PostgreSQL"""
        user = User.objects.create_user(
            username='testdbuser',
            email='testdb@example.com',
            password='testdbpass123'
        )
        self.assertEqual(user.username, 'testdbuser')
        self.assertTrue(user.check_password('testdbpass123'))
        
        # Verificar se consegue buscar do banco
        retrieved_user = User.objects.get(username='testdbuser')
        self.assertEqual(retrieved_user.email, 'testdb@example.com')


@pytest.mark.django_db
class TestDashboardWithPytest:
    """Testes do dashboard usando pytest"""
    
    def test_dashboard_redirect_pytest(self, client):
        """Teste de redirecionamento do dashboard com pytest"""
        user = User.objects.create_user(
            username='pytestdashboard',
            email='pytestdashboard@example.com',
            password='pytestpass123'
        )
        
        # Teste sem login
        response = client.get('/dashboard/')
        assert response.status_code == 302
        assert '/accounts/login/' in response.url
        
        # Teste com login
        client.force_login(user)
        response = client.get('/dashboard/')
        assert response.status_code == 302
        assert response.url == '/dashboard/executivo/'
    
    def test_database_postgresql_pytest(self):
        """Teste para verificar se está usando PostgreSQL"""
        from django.db import connection
        
        # Verificar se está usando PostgreSQL
        assert 'postgresql' in connection.settings_dict['ENGINE']
        
        # Testar conexão
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        result = cursor.fetchone()
        assert 'PostgreSQL' in result[0]
