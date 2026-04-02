# AJURES Backend - Sistema de Gestao Juridica

Backend Django para sistema de gestao de escritorio de advocacia.

## Tecnologias

- **Django 5.0.14**
- **Python 3.11+**
- **PostgreSQL** (Banco de dados principal)
- **Django REST Framework** (API REST)
- **python-decouple** (Gerenciamento de variaveis de ambiente)
- **psycopg2** (Driver PostgreSQL)

## Estrutura do Projeto

```
ajures_back/
├── config/              # Configuracoes do Django
│   ├── settings.py      # Configuracoes principais
│   ├── urls.py          # URLs principais
│   ├── wsgi.py          # WSGI para producao
│   └── asgi.py          # ASGI para async
├── accounts/            # Autenticacao e usuarios
├── clientes/            # Gestao de clientes
├── processos/           # Gestao de processos
├── andamentos/          # Andamentos processuais
├── agenda/              # Agenda e compromissos
├── financeiro/          # Gestao financeira
├── documentos/          # Gestao de documentos
├── notifications/       # Sistema de notificacoes
├── portal/              # Portal do cliente
├── dashboard/           # Dashboard e relatorios
├── core/                # Funcionalidades core
├── templatesmsg/        # Templates de mensagens
├── static/              # Arquivos estaticos
├── media/               # Arquivos de upload
├── templates/           # Templates HTML
├── manage.py            # Gerenciador Django
├── requirements.txt     # Dependencias Python
├── .env                 # Variaveis de ambiente (NAO COMMITAR)
└── .env.example         # Exemplo de variaveis de ambiente
```

## Configuracao do Ambiente

### 1. Pre-requisitos

- Python 3.11 ou superior
- PostgreSQL 12 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalacao

#### 2.1. Clone o repositorio (se aplicavel)

```bash
git clone <url-do-repositorio>
cd ajures_back
```

#### 2.2. Crie um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.3. Instale as dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuracao do Banco de Dados

#### 3.1. Crie o banco de dados PostgreSQL

```sql
CREATE DATABASE db_test;
CREATE USER dbTester WITH PASSWORD 'T3$t1ng';
GRANT ALL PRIVILEGES ON DATABASE db_test TO dbTester;
```

#### 3.2. Configure o arquivo .env

**IMPORTANTE:** O arquivo `.env` deve estar na raiz do projeto (mesmo diretorio do `manage.py`)

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configuracoes:

```env
# Django Configuration
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database Configuration
DB_NAME=db_test
DB_USER=dbTester
DB_PASSWORD=T3$t1ng
DB_HOST=localhost
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**ATENCAO - Evitando UnicodeDecodeError:**

1. **Use apenas caracteres ASCII nos comentarios do .env**
   - ERRADO: `# Configuracoes do Django`
   - CORRETO: `# Django Configuration`

2. **Nao use acentos ou caracteres especiais nos comentarios**
   - Evite: c, a, o, a, e, i, o, u

3. **Salve o arquivo .env com encoding UTF-8 SEM BOM**
   - No VS Code: `File > Save with Encoding > UTF-8`
   - No Notepad++: `Encoding > Encode in UTF-8 (without BOM)`

4. **Nunca use aspas duplas desnecessarias nos valores**
   - ERRADO: `DB_PASSWORD="T3$t1ng"`
   - CORRETO: `DB_PASSWORD=T3$t1ng`

### 4. Execute as migracoes

```bash
python manage.py migrate
```

### 5. Crie um superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 6. Execute o servidor de desenvolvimento

```bash
python manage.py runserver
```

O servidor estara disponivel em: `http://localhost:8000`

## Testes e Validacao

### Verificar configuracao

```bash
python manage.py check
```

### Executar testes

```bash
pytest
```

## Solucao de Problemas

### Erro: UnicodeDecodeError

**Sintoma:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe7 in position 78
```

**Causa:**
O arquivo `.env` contem caracteres nao-ASCII (acentos) nos comentarios.

**Solucao:**
1. Abra o arquivo `.env` em um editor de texto
2. Remova todos os acentos dos comentarios
3. Salve o arquivo com encoding UTF-8 SEM BOM
4. Use o arquivo `.env` fornecido neste projeto (ja corrigido)

### Erro: python-decouple nao encontra o .env

**Sintoma:**
```
django.core.exceptions.ImproperlyConfigured: Set the DB_NAME environment variable
```

**Solucao:**
1. Certifique-se de que o arquivo `.env` esta na raiz do projeto
2. Verifique se voce esta executando `python manage.py` da raiz do projeto
3. Confirme que o `.env` nao esta sendo ignorado pelo `.gitignore`

### Erro: Conexao com PostgreSQL falha

**Sintoma:**
```
django.db.utils.OperationalError: could not connect to server
```

**Solucao:**
1. Verifique se o PostgreSQL esta rodando
2. Confirme as credenciais no arquivo `.env`
3. Teste a conexao manualmente:
   ```bash
   psql -U dbTester -d db_test -h localhost
   ```

## Boas Praticas

### Variaveis de Ambiente

1. **NUNCA commite o arquivo `.env`** - ele contem informacoes sensiveis
2. **Sempre use `.env.example`** como template
3. **Use apenas ASCII** nos comentarios do `.env`
4. **Mantenha senhas complexas** em producao

### Desenvolvimento

1. **Sempre ative o ambiente virtual** antes de trabalhar
2. **Execute `python manage.py check`** antes de commitar
3. **Mantenha as dependencias atualizadas** no `requirements.txt`
4. **Use migrations** para todas as alteracoes no banco de dados

### Seguranca

1. **DEBUG=False** em producao
2. **SECRET_KEY** unica e complexa em producao
3. **ALLOWED_HOSTS** configurado corretamente
4. **Use HTTPS** em producao

## Documentacao Adicional

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [python-decouple](https://github.com/henriquebastos/python-decouple)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
