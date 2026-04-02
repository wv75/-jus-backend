from django.contrib.auth.models import User
from django.db                  import transaction
from rest_framework             import serializers
from .models                    import Advogado


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model            = User
        fields           = ['id', 'username', 'email', 'last_login', 'first_name', 'last_name']
        read_only_fields = fields


class AdvogadoCreateSerializer(serializers.ModelSerializer):
    username       = serializers.CharField(write_only=True, required=True, max_length=150)
    password       = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    especialidades = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model        = Advogado
        fields       = [
            'id', 'username', 'password', 'nome', 'sobrenome', 'cpf', 'rg',
            'data_nascimento', 'sexo', 'estado_civil', 'telefone_celular', 'telefone_fixo',
            'email', 'email_citacao', 'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'uf', 'pais', 'oab_numero', 'oab_uf', 'cargo',
            'nivel_profissional', 'area_atuacao_principal', 'especialidades',
            'descricao_profissional', 'supervisor', 'tipo_contrato', 'valor_hora',
            'pix_chave', 'banco_nome', 'agencia', 'conta', 'tipo_conta', 'cpf_cnpj_conta',
            'documentos', 'documentos_pendentes', 'termo_assinado', 'ativo',
        ]
        extra_kwargs = {
            'documentos': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        user_data          = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'email'   : validated_data.get('email')
        }
        advogado_data      = validated_data
        especialidades_str = advogado_data.pop('especialidades', None)

        if especialidades_str:
            advogado_data['especialidades'] = [s.strip() for s in especialidades_str.split(',') if s.strip()]
        elif especialidades_str == '':
            advogado_data['especialidades'] = []

        try:
            with transaction.atomic():
                user            = User.objects.create_user(**user_data)
                documentos_data = advogado_data.pop('documentos', [])
                advogado        = Advogado.objects.create(usuario=user, **advogado_data)

                if documentos_data:
                    advogado.documentos.set(documentos_data)

                return advogado

        except Exception as e:
            raise serializers.ValidationError(f"Erro ao criar usuário e perfil: {e}")


class AdvogadoSimpleSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model  = Advogado
        fields = ['id', 'full_name']


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model            = User
        fields           = ['username', 'email']
        read_only_fields = fields


class AdvogadoListSerializer(serializers.ModelSerializer):
    usuario = UserNestedSerializer(read_only=True)

    class Meta:
        model            = Advogado
        fields           = ['id', 'nome', 'sobrenome', 'cargo', 'ativo', 'usuario']
        read_only_fields = fields