from rest_framework import serializers
from .models        import Cliente, PessoaFisica, PessoaJuridica


class ClienteBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Cliente
        fields           = ['id', 'tipo', 'canal_preferido', 'consentimento_lgpd', 'data_consentimento', 'advogado', 'ativo']
        read_only_fields = ['id', 'tipo', 'data_consentimento']


class PessoaFisicaSerializer(serializers.ModelSerializer):
    cliente_id         = serializers.IntegerField(source='cliente.id', read_only=True)
    canal_preferido    = serializers.CharField(source='cliente.canal_preferido')
    consentimento_lgpd = serializers.BooleanField(source='cliente.consentimento_lgpd')
    advogado           = serializers.PrimaryKeyRelatedField(source='cliente.advogado', read_only=True)

    class Meta:
        model            = PessoaFisica
        fields           = [
            'id', 'cliente_id', 'nome_completo', 'cpf', 'telefone', 'email', 'estado_civil', 
            'profissao', 'nacionalidade', 'rne', 'nome_mae', 'nome_pai', 'cep', 'logradouro', 
            'numero', 'bairro', 'cidade', 'estado', 'canal_preferido', 'consentimento_lgpd', 
            'advogado', 'ativo'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente', {})
        cliente      = Cliente.objects.create(tipo='PF', **cliente_data)
        return PessoaFisica.objects.create(cliente=cliente, **validated_data)

    def update(self, instance, validated_data):
        cliente_data = validated_data.pop('cliente', {})
        if cliente_data:
            for attr, value in cliente_data.items():
                setattr(instance.cliente, attr, value)
            instance.cliente.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PessoaJuridicaSerializer(serializers.ModelSerializer):
    cliente_id         = serializers.IntegerField(source='cliente.id', read_only=True)
    canal_preferido    = serializers.CharField(source='cliente.canal_preferido')
    consentimento_lgpd = serializers.BooleanField(source='cliente.consentimento_lgpd')
    advogado           = serializers.PrimaryKeyRelatedField(source='cliente.advogado', read_only=True)

    class Meta:
        model            = PessoaJuridica
        fields           = [
            'id', 'cliente_id', 'razao_social', 'cnpj', 'representante', 'cep', 'logradouro', 
            'numero', 'bairro', 'cidade', 'estado', 'canal_preferido', 'consentimento_lgpd', 
            'advogado', 'ativo'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente', {})
        cliente      = Cliente.objects.create(tipo='PJ', **cliente_data)
        return PessoaJuridica.objects.create(cliente=cliente, **validated_data)

    def update(self, instance, validated_data):
        cliente_data = validated_data.pop('cliente', {})
        if cliente_data:
            for attr, value in cliente_data.items():
                setattr(instance.cliente, attr, value)
            instance.cliente.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance