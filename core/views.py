from django.core import exceptions

class CompanySafeViewMixin:
    """ 
    Mixin para ser usado com views que garante que os modelos estejam 
    relacionados à empresa durante a criação e que os querysets sejam 
    filtrados para operações de leitura.
    """
    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_authenticated:
            raise exceptions.NotAuthenticated()
        
        company_id = self.request.user.company_id
        return queryset.filter(company_id=company_id)
    
    def perform_create(self, serializer):
        company_id = self.request.user.company_id
        serializer.save(company_id=company_id)

        