import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse


class APIAuthenticationTestCase(TestCase):
    """Testes para autenticação da API"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
        self.token = Token.objects.create(user=self.user)
    
    def test_api_without_authentication(self):
        """Testa acesso à API sem autenticação"""
        response = self.client.get('/api/resumo-financeiro/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_api_with_token_authentication(self):
        """Testa acesso à API com token de autenticação"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/resumo-financeiro/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_with_session_authentication(self):
        """Testa acesso à API com autenticação de sessão"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/resumo-financeiro/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FinanceiroAPITestCase(TestCase):
    """Testes para API financeira"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='financeirouser',
            email='financeiro@example.com',
            password='financeiropass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_resumo_financeiro_endpoint(self):
        """Testa endpoint de resumo financeiro"""
        response = self.client.get('/api/resumo-financeiro/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se retorna os campos esperados
        data = response.json()
        expected_fields = [
            'receitas_pagas', 'despesas_pagas', 'saldo_atual',
            'contas_receber', 'contas_pagar', 'honorarios_pendentes'
        ]
        for field in expected_fields:
            self.assertIn(field, data)
    
    def test_resumo_financeiro_mensal_endpoint(self):
        """Testa endpoint de resumo financeiro mensal"""
        response = self.client.get('/api/resumo-financeiro/mensal/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se retorna os campos esperados
        data = response.json()
        expected_fields = ['ano', 'mes', 'receitas_mes', 'despesas_mes', 'saldo_mes']
        for field in expected_fields:
            self.assertIn(field, data)
    
    def test_plano_contas_list(self):
        """Testa listagem de plano de contas"""
        response = self.client.get('/api/plano-contas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar uma lista (mesmo que vazia)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)  # Paginação ativa
    
    def test_contas_bancarias_list(self):
        """Testa listagem de contas bancárias"""
        response = self.client.get('/api/contas-bancarias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar uma lista (mesmo que vazia)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)  # Paginação ativa
    
    def test_movimentacoes_list(self):
        """Testa listagem de movimentações financeiras"""
        response = self.client.get('/api/movimentacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar uma lista (mesmo que vazia)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)  # Paginação ativa
    
    def test_honorarios_list(self):
        """Testa listagem de honorários"""
        response = self.client.get('/api/honorarios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar uma lista (mesmo que vazia)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)  # Paginação ativa


class AgendaAPITestCase(TestCase):
    """Testes para API da agenda"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='agendauser',
            email='agenda@example.com',
            password='agendapass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_tipos_compromisso_list(self):
        """Testa listagem de tipos de compromisso"""
        response = self.client.get('/api/tipos-compromisso/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar uma lista (mesmo que vazia)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)  # Paginação ativa
    
    def test_compromissos_list(self):
        """Testa listagem de compromissos"""
        response = self.client.get('/api/compromissos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar uma lista (mesmo que vazia)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)  # Paginação ativa
    
    def test_compromissos_hoje_endpoint(self):
        """Testa endpoint de compromissos de hoje"""
        response = self.client.get('/api/compromissos/hoje/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar uma lista
        data = response.json()
        self.assertIsInstance(data, list)
    
    def test_compromissos_proximos_endpoint(self):
        """Testa endpoint de próximos compromissos"""
        response = self.client.get('/api/compromissos/proximos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar uma lista
        data = response.json()
        self.assertIsInstance(data, list)


@pytest.mark.django_db
class TestAPIWithPytest:
    """Testes da API usando pytest"""
    
    def test_api_endpoints_require_auth(self):
        """Testa se endpoints da API requerem autenticação"""
        client = APIClient()
        
        endpoints = [
            '/api/resumo-financeiro/',
            '/api/plano-contas/',
            '/api/contas-bancarias/',
            '/api/movimentacoes/',
            '/api/honorarios/',
            '/api/tipos-compromisso/',
            '/api/compromissos/',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_api_with_authentication(self):
        """Testa API com autenticação"""
        client = APIClient()
        user = User.objects.create_user(
            username='pytestapi',
            email='pytestapi@example.com',
            password='pytestpass123'
        )
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = client.get('/api/resumo-financeiro/')
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert 'receitas_pagas' in data
        assert 'despesas_pagas' in data
        assert 'saldo_atual' in data
