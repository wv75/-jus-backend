#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico Premium de Encoding e Configuração Django
Identifica problemas de UnicodeDecodeError em ambientes Windows/PostgreSQL
"""

import os
import sys
from pathlib import Path

print("=" * 80)
print("DIAGNÓSTICO PREMIUM - AUDITORIA DE ENCODING E CONFIGURAÇÃO")
print("=" * 80)

# 1. VERIFICAR AMBIENTE
print("\n[1] AMBIENTE DO SISTEMA")
print("-" * 80)
print(f"Python Version: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"Default Encoding: {sys.getdefaultencoding()}")
print(f"Filesystem Encoding: {sys.getfilesystemencoding()}")
print(f"Current Working Directory: {os.getcwd()}")

# 2. VERIFICAR ARQUIVOS .env
print("\n[2] ARQUIVOS .env ENCONTRADOS")
print("-" * 80)

env_files = []
for root, dirs, files in os.walk('.'):
    # Ignorar diretórios específicos
    dirs[:] = [d for d in dirs if d not in ['.git', '.nvm', '__pycache__', 'venv', 'env']]
    for file in files:
        if file.startswith('.env'):
            env_files.append(os.path.join(root, file))

for env_file in env_files:
    print(f"\n  Arquivo: {env_file}")
    
    # Verificar encoding
    try:
        with open(env_file, 'rb') as f:
            raw_content = f.read()
        
        # Verificar BOM
        has_bom = raw_content.startswith(b'\xef\xbb\xbf')
        print(f"    - Tamanho: {len(raw_content)} bytes")
        print(f"    - BOM UTF-8: {'SIM ⚠️' if has_bom else 'NÃO ✓'}")
        
        # Verificar se é UTF-8 válido
        try:
            decoded = raw_content.decode('utf-8')
            print(f"    - UTF-8 válido: SIM ✓")
        except UnicodeDecodeError as e:
            print(f"    - UTF-8 válido: NÃO ⚠️")
            print(f"    - Erro: {e}")
        
        # Procurar caracteres não-ASCII
        non_ascii_chars = []
        for i, byte in enumerate(raw_content):
            if byte >= 128:
                non_ascii_chars.append((i, byte))
        
        if non_ascii_chars:
            print(f"    - Caracteres não-ASCII: {len(non_ascii_chars)} encontrados ⚠️")
            # Mostrar primeiros 5
            for i, (pos, byte) in enumerate(non_ascii_chars[:5]):
                context_start = max(0, pos-10)
                context_end = min(len(raw_content), pos+10)
                context = raw_content[context_start:context_end]
                print(f"      Posição {pos}: 0x{byte:02x} - Contexto: {context}")
        else:
            print(f"    - Caracteres não-ASCII: Nenhum ✓")
            
    except Exception as e:
        print(f"    - ERRO ao ler arquivo: {e}")

# 3. TESTAR DECOUPLE
print("\n[3] TESTE DE LEITURA COM PYTHON-DECOUPLE")
print("-" * 80)

try:
    from decouple import config, AutoConfig
    
    # Verificar qual .env está sendo usado
    auto_config = AutoConfig()
    print(f"  AutoConfig search_path: {auto_config.search_path if hasattr(auto_config, 'search_path') else 'N/A'}")
    
    # Testar leitura de variáveis
    test_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'SECRET_KEY', 'DEBUG']
    
    for var in test_vars:
        try:
            value = config(var, default='NOT_FOUND')
            # Mascarar senhas
            if 'PASSWORD' in var or 'SECRET' in var:
                display_value = value[:3] + '***' if len(value) > 3 else '***'
            else:
                display_value = value
            
            # Verificar encoding do valor
            try:
                value.encode('ascii')
                encoding_status = "ASCII ✓"
            except UnicodeEncodeError:
                encoding_status = "NON-ASCII ⚠️"
            
            print(f"  {var}: {display_value} ({encoding_status})")
            
        except Exception as e:
            print(f"  {var}: ERRO - {e}")
            
except ImportError:
    print("  ⚠️ python-decouple não instalado")
except Exception as e:
    print(f"  ⚠️ Erro ao testar decouple: {e}")

# 4. VERIFICAR SETTINGS.PY
print("\n[4] ANÁLISE DO SETTINGS.PY")
print("-" * 80)

settings_path = Path('config/settings.py')
if settings_path.exists():
    print(f"  Arquivo encontrado: {settings_path}")
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings_content = f.read()
        
        # Verificar imports
        if 'from decouple import' in settings_content:
            print("  ✓ Importa decouple")
        else:
            print("  ⚠️ NÃO importa decouple")
        
        # Verificar BASE_DIR
        if 'BASE_DIR' in settings_content:
            print("  ✓ Define BASE_DIR")
        else:
            print("  ⚠️ NÃO define BASE_DIR")
            
        # Verificar configuração de DB
        if 'postgresql' in settings_content.lower():
            print("  ✓ Configurado para PostgreSQL")
        else:
            print("  ⚠️ PostgreSQL não detectado")
            
    except Exception as e:
        print(f"  ⚠️ Erro ao ler settings.py: {e}")
else:
    print(f"  ⚠️ Arquivo não encontrado: {settings_path}")

# 5. VERIFICAR ESTRUTURA DO PROJETO
print("\n[5] ESTRUTURA DO PROJETO")
print("-" * 80)

required_files = ['manage.py', 'config/settings.py', 'config/__init__.py', '.env']
for file in required_files:
    exists = Path(file).exists()
    status = "✓" if exists else "⚠️ FALTANDO"
    print(f"  {file}: {status}")

# 6. SIMULAR CONEXÃO POSTGRESQL (sem conectar de verdade)
print("\n[6] SIMULAÇÃO DE CONEXÃO POSTGRESQL")
print("-" * 80)

try:
    from decouple import config
    
    db_params = {
        'dbname': config('DB_NAME', default=''),
        'user': config('DB_USER', default=''),
        'password': config('DB_PASSWORD', default=''),
        'host': config('DB_HOST', default=''),
        'port': config('DB_PORT', default='5432'),
    }
    
    print("  Parâmetros de conexão:")
    for key, value in db_params.items():
        if key == 'password':
            display = value[:3] + '***' if len(value) > 3 else '***'
        else:
            display = value
        
        # Testar encoding
        try:
            if isinstance(value, str):
                value.encode('utf-8')
                encoded = value.encode('utf-8')
                # Verificar se tem caracteres problemáticos
                try:
                    encoded.decode('ascii')
                    enc_status = "ASCII"
                except:
                    enc_status = "UTF-8"
            else:
                enc_status = "N/A"
        except Exception as e:
            enc_status = f"ERRO: {e}"
        
        print(f"    {key}: {display} [{enc_status}]")
        
except Exception as e:
    print(f"  ⚠️ Erro ao simular conexão: {e}")

print("\n" + "=" * 80)
print("DIAGNÓSTICO CONCLUÍDO")
print("=" * 80)
