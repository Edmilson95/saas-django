from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Company

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'password',
        )
        # Certifique-se que o campo password nunca é enviado de volta ao cliente
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        updated = super().update(instance, validated_data)

        # Nós salvamos o usuario novamente se a password foi especificada para garantir que ela seja devidamente criptografada
        if 'password' in validated_data:
            updated.set_password(validated_data['password'])
            updated.save()
        return updated

class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'address',
        )

class AccountSerializer(serializers.Serializer):
    """Serializer que tem dois Serializers aninhados: company e user"""

    company = CompanySerializer()
    user = UserSerializer()

    def create(self, validated_data):
        company_data = validated_data['company']
        user_data = validated_data['user']

        # Chama nosso CompanyManager para criar a Company e o User
        company, user = Company.objects.create_account(
            company_name=company_data.get('name'),
            company_address=company_data.get('address'),
            username=user_data.get('username'),
            password=user_data.get('password'),
        )

        return {'company': company, 'user': user}
    
    def update(self, instance, validated_data):
        raise NotImplementedError('Não é possível chamar update() em uma conta')