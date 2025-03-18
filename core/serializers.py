from rest_framework import serializers

class CompanySafeRelatedField(serializers.HyperlinkedRelatedField):
    """
    Garante que o queryset retorna apenas valor para uma empresa
    """
    def get_queryset(self):
        request = self.context['request']
        company_id = request.user.company_id
        return super().get_queryset().filter(company_id=company_id)
    
class CompanySafeSerializerMixin(object):
    """
    Mixin to be used with HyperlinkedModelSerializer to ensure that only company values are returned 
    """
    serializer_related_field = CompanySafeRelatedField