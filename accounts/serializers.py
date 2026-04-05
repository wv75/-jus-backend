from django.contrib.auth.models import User, Group
from rest_framework             import serializers
from .models                    import Advogado


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']


class UserManagerSerializer(serializers.ModelSerializer):
    groups   = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'groups', 'password']

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        password    = validated_data.pop('password', None)
        
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        
        user.groups.set(groups_data)
        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        password    = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        instance.save()

        if groups_data is not None:
            instance.groups.set(groups_data)
            
        return instance


class AdvogadoSimpleSerializer(serializers.ModelSerializer):
    nome_completo = serializers.SerializerMethodField()

    class Meta:
        model  = Advogado
        fields = ['id', 'nome', 'sobrenome', 'nome_completo', 'cargo', 'ativo']

    def get_nome_completo(self, obj):
        return f"{obj.nome} {obj.sobrenome}"


class AdvogadoListSerializer(serializers.ModelSerializer):
    usuario_email    = serializers.CharField(source='usuario.email', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    supervisor_nome  = serializers.SerializerMethodField()
    criado_por_nome  = serializers.CharField(source='criado_por.username', read_only=True)

    class Meta:
        model  = Advogado
        fields = [
            'id', 'nome', 'sobrenome', 'cargo', 'ativo', 'usuario', 
            'usuario_email', 'usuario_username', 'supervisor', 'supervisor_nome', 
            'criado_por_nome'
        ]

    def get_supervisor_nome(self, obj):
        if hasattr(obj, 'supervisor') and obj.supervisor:
            return f"{obj.supervisor.nome} {obj.supervisor.sobrenome}"
        return None


class AdvogadoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Advogado
        fields = '__all__'