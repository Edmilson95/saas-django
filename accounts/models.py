import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

class CompanyManager(models.Manager): # Fornece um método create_account que garante que uma Company seja sempre criada com um User atribuído a ela.
    """Manager do model Company. Também lida com a criação de accounts"""

    @transaction.atomic
    def create_account(self, company_name, username, password, company_address=None):
        """Cria uma Company juntamente com um User e retorna ambos"""
        
        company = Company(
            name=company_name,
            address=company_address,
        )
        company.save()

        user = User.objects.create_user(
            username=username,
            password=password,
            company=company,
        )

        return company, user
    
class Company(models.Model): # Este é o modelo que representa a conta SaaS
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length=100)
    address = models.CharField('address', max_length=250, blank=True)

    objects = CompanyManager()

    class Meta: # Prefira sempre nomear manualmente as tabelas do banco de dados
        db_table = 'companies'

    def __str__(self):
        return self.name
    
class User(AbstractUser): # Modelo de Usuário personalizado. É recomendado não usar o modelo de Usuário fornecido pelo Django e criar um personalizado.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, related_name='%(class)s', on_delete=models.CASCADE, editable=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'({self.company.name}) - {self.username}'
    