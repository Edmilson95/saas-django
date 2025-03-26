from rest_framework import serializers
from core.serializers import CompanySafeSerializerMixin
from .models import UserMessage

class UserMessageSerializer(CompanySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserMessage
        fields = ( # Define quais dados serão incluídos na resposta.
            'id',
            'url',
            'from_user',
            'to_user',
            'text',
            'date',
        )
        read_only_fields = ( # só leitura, então não pode ser alterado pelo usuário
            'from_user',
        )
