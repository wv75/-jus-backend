# Dockerfile

# 1. Imagem Base: Começamos com uma imagem oficial e leve do Python.
FROM python:3.10-slim

# 2. Variáveis de Ambiente: Boas práticas para rodar Python no Docker.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Diretório de Trabalho: Define onde nossa aplicação vai ficar dentro do contêiner.
WORKDIR /app

# 4. Instalação de Dependências: Copiamos apenas o requirements.txt primeiro.
# Isso aproveita o cache do Docker; se não mudarmos as dependências, ele não reinstala tudo.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o Código: Agora copiamos todo o resto do projeto para dentro do contêiner.
COPY . .

# 6. Coletar Arquivos Estáticos: Rodamos o comando collectstatic para que o Whitenoise os encontre.
RUN SECRET_KEY='dummy-key-for-build' COLLECTING_STATIC=True python manage.py collectstatic --noinput --clear

# 7. Expor a Porta: Informamos ao Docker que nossa aplicação rodará na porta 8000.
EXPOSE 8000

# 8. Comando de Início: Este é o comando que inicia o servidor Gunicorn quando o contêiner é executado.
#    Aponte para o arquivo wsgi do seu projeto. O seu está em 'config/wsgi.py'.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
