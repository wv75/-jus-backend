# core/views.py

from django.shortcuts import render
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# --- INÍCIO DA CORREÇÃO ---
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
# --- FIM DA CORREÇÃO ---


def landing_view(request):
    """
    View para a landing page principal.
    Esta página NÃO faz parte da aplicação Vue e é servida diretamente pelo Django.
    """
    return render(request, 'landing.html')

def vue_app_view(request, *args, **kwargs):
    """
    Esta é a view "coringa" que serve a aplicação Vue.js.
    Todas as rotas da sua aplicação principal (ex: /dashboard, /clientes, /processos/123)
    deverão apontar para esta única view. O Vue Router cuidará do resto no frontend.
    """
    return render(request, 'index.html')

class LogoutAPIView(APIView):
    """
    Endpoint de API para fazer logout do usuário.
    O Vue.js chamará esta URL com um método POST. Em caso de sucesso,
    o próprio frontend redirecionará o usuário para a página de login/landing.
    """
    
    # --- INÍCIO DA CORREÇÃO ---

    # 1. ESPECIFICAR O MÉTODO DE AUTENTICAÇÃO
    #    Isso força o DRF a usar *apenas* TokenAuthentication para esta view,
    #    ignorando a SessionAuthentication (que é a causa do 403 por CSRF).
    authentication_classes = [TokenAuthentication]
    
    # 2. MANTER A PERMISSÃO CORRETA
    #    (Isso já estava correto no seu arquivo)
    permission_classes = [IsAuthenticated]
    
    # --- FIM DA CORREÇÃO ---


    def post(self, request, *args, **kwargs):
        
        # --- INÍCIO DA CORREÇÃO ---
            
        # 3. IMPLEMENTAR A LÓGICA DE LOGOUT CORRETA
        #    A lógica principal para TokenAuth é DELETAR o token.
        try:
            # Deleta o token de autenticação da API do banco de dados
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            # Lida com casos onde o token não existe ou o auth_token
            # não está configurado. Não quebre a aplicação por isso.
            pass
        
        # 4. MANTER O LOGOUT DE SESSÃO
        #    Isso é uma boa prática (defesa em profundidade) para
        #    limpar qualquer sessão do Django (ex: /admin) que possa existir.
        logout(request)
        
        # --- FIM DA CORREÇÃO ---
        
        return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)