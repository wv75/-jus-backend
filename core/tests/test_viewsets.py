import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from agenda.models import TipoCompromisso, Compromisso
from financeiro.models import PlanoContas, ContaBancaria, MovimentacaoFinanceira, Honorario
from clientes.models import Cliente
from datetime import datetime, timedelta
from django.utils import timezone


class AgendaViewSetsTestCase(TestCase):
    """Testes para ViewSets da agenda"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='agendatest',
            email='agenda@test.com',
            password='agendapass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Criar dados de teste
        self.tipo_compromisso = TipoCompromisso.objects.create(
            nome='Audiência',
            cor='#ff0000'
        )
        
        self.compromisso = Compromisso.objects.create(
            titulo='Audiência de Conciliação',
            descricao='Audiência no Fórum Central',
            data_inicio=timezone.now(),
            data_fim=timezone.now() + timedelta(hours=1),
            tipo=self.tipo_compromisso,
            responsavel=self.user,
            prioridade='alta'
        )
    
    def test_tipos_compromisso_list(self):
        """Testa listagem de tipos de compromisso"""
        response = self.client.get('/api/tipos-compromisso/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nome'], 'Audiência')
    
    def test_tipos_compromisso_create(self):
        """Testa criação de tipo de compromisso"""
        data = {
            'nome': 'Reunião',
            'cor': '#00ff00',
            'ativo': True
        }
        response = self.client.post('/api/tipos-compromisso/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TipoCompromisso.objects.count(), 2)
    
    def test_compromissos_list(self):
        """Testa listagem de compromissos"""
        response = self.client.get('/api/compromissos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['titulo'], 'Audiência de Conciliação')
    
    def test_compromissos_hoje(self):
        """Testa endpoint de compromissos de hoje"""
        response = self.client.get('/api/compromissos/hoje/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        # Deve retornar o compromisso criado hoje
        self.assertEqual(len(data), 1)
    
    def test_compromissos_proximos(self):
        """Testa endpoint de próximos compromissos"""
        response = self.client.get('/api/compromissos/proximos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        # Deve retornar o compromisso dos próximos 7 dias
        self.assertEqual(len(data), 1)


class FinanceiroViewSetsTestCase(TestCase):
    """Testes para ViewSets do financeiro"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='financeirotest',
            email='financeiro@test.com',
            password='financeiropass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Criar dados de teste
        self.plano_conta = PlanoContas.objects.create(
            codigo='1.1.001',
            nome='Receitas de Honorários',
            tipo='receita'
        )
        
        self.conta_bancaria = ContaBancaria.objects.create(
            nome='Conta Corrente Principal',
            banco='Banco do Brasil',
            agencia='1234',
            conta='56789-0',
            saldo_inicial=10000.00
        )
        
        # Criar cliente para testes
        self.cliente = Cliente.objects.create(
            nome='Cliente Teste',
            documento='12345678901',
            email='cliente@test.com',
            telefone='11999999999'
        )
        
        self.movimentacao = MovimentacaoFinanceira.objects.create(
            tipo='receita',
            descricao='Honorários Advocatícios',
            valor=5000.00,
            data_vencimento=timezone.now().date(),
            conta_bancaria=self.conta_bancaria,
            plano_conta=self.plano_conta,
            cliente=self.cliente,
            responsavel=self.user,
            status='pago'
        )
        
        self.honorario = Honorario.objects.create(
            cliente=self.cliente,
            descricao='Consultoria Jurídica',
            tipo='fixo',
            valor=3000.00,
            data_vencimento=timezone.now().date(),
            advogado=self.user,
            status='aprovado'
        )
    
    def test_plano_contas_list(self):
        """Testa listagem de plano de contas"""
        response = self.client.get('/api/plano-contas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['codigo'], '1.1.001')
    
    def test_contas_bancarias_list(self):
        """Testa listagem de contas bancárias"""
        response = self.client.get('/api/contas-bancarias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nome'], 'Conta Corrente Principal')
    
    def test_movimentacoes_list(self):
        """Testa listagem de movimentações financeiras"""
        response = self.client.get('/api/movimentacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['descricao'], 'Honorários Advocatícios')
    
    def test_honorarios_list(self):
        """Testa listagem de honorários"""
        response = self.client.get('/api/honorarios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['descricao'], 'Consultoria Jurídica')
    
    def test_resumo_financeiro(self):
        """Testa endpoint de resumo financeiro"""
        response = self.client.get('/api/resumo-financeiro/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Verificar campos obrigatórios
        expected_fields = [
            'receitas_pagas', 'despesas_pagas', 'saldo_atual',
            'contas_receber', 'contas_pagar', 'honorarios_pendentes'
        ]
        for field in expected_fields:
            self.assertIn(field, data)
        
        # Verificar valores calculados
        self.assertEqual(data['receitas_pagas'], 5000.0)
        self.assertEqual(data['despesas_pagas'], 0.0)
        self.assertEqual(data['saldo_atual'], 5000.0)
    
    def test_resumo_financeiro_mensal(self):
        """Testa endpoint de resumo financeiro mensal"""
        ano = timezone.now().year
        mes = timezone.now().month
        response = self.client.get(f'/api/resumo-financeiro/mensal/?ano={ano}&mes={mes}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Verificar campos obrigatórios
        expected_fields = ['ano', 'mes', 'receitas_mes', 'despesas_mes', 'saldo_mes']
        for field in expected_fields:
            self.assertIn(field, data)
        
        self.assertEqual(data['ano'], ano)
        self.assertEqual(data['mes'], mes)


@pytest.mark.django_db
class TestViewSetsWithPytest:
    """Testes dos ViewSets usando pytest"""
    
    def test_agenda_viewsets_require_auth(self):
        """Testa se ViewSets da agenda requerem autenticação"""
        client = APIClient()
        
        endpoints = [
            '/api/tipos-compromisso/',
            '/api/compromissos/',
            '/api/compromissos/hoje/',
            '/api/compromissos/proximos/',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_financeiro_viewsets_require_auth(self):
        """Testa se ViewSets do financeiro requerem autenticação"""
        client = APIClient()
        
        endpoints = [
            '/api/plano-contas/',
            '/api/contas-bancarias/',
            '/api/movimentacoes/',
            '/api/honorarios/',
            '/api/resumo-financeiro/',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_viewsets_with_authentication(self):
        """Testa ViewSets com autenticação"""
        client = APIClient()
        user = User.objects.create_user(
            username='pytestviewsets',
            email='pytestviewsets@test.com',
            password='pytestpass123'
        )
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        # Testar endpoints principais
        endpoints = [
            '/api/tipos-compromisso/',
            '/api/compromissos/',
            '/api/plano-contas/',
            '/api/contas-bancarias/',
            '/api/movimentacoes/',
            '/api/honorarios/',
            '/api/resumo-financeiro/',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            if endpoint != '/api/resumo-financeiro/':
                assert 'results' in data  # Paginação ativa
            else:
                assert isinstance(data, dict)  # Resumo é um dict direto
