from rest_framework import serializers

class CompanySafeRelatedField(serializers.HyperlinkedRelatedField): # Garante que o queryset retorne apenas valores para a empresa
    
    def get_queryset(self): # filtra os resultados pela empresa do usuário logado.
        request = self.context['request']
        company_id = request.user.company_id
        return super().get_queryset().filter(company_id=company_id)
    
class CompanySafeSerializerMixin(object): # Mixin a ser usado com o HyperlinkedModelSerializer para garantir que apenas os valores da empresa sejam retornados.
    serializer_related_field = CompanySafeRelatedField