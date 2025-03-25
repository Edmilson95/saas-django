from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from . import serializers

User = get_user_model()

class AccountCreate(generics.CreateAPIView): # Herda de CreateAPIView, então não haverá como listar ou atualizar as contas.
    name = 'account-create'
    serializer_class = serializers.AccountSerializer

class UserList(generics.ListCreateAPIView):
    name = 'user-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        company_id = self.request.user.company_id
        serializer.save(company_id=company_id)

    def get_queryset(self): # Sobrescreve o método get_queryset para retornar apenas os resultados relacionados à empresa do usuário que está fazendo a solicitação.
        company_id = self.request.user.company_id
        return super().get_queryset().filter(company_id=company_id)
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'user-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_queryset(self): # Sobrescreve o método get_queryset da mesma forma que a view UserList (vamos abordar isso mais tarde). Se você tentar obter um usuário de outra empresa, receberá uma resposta 404 Not Found.
        company_id = self.request.user.company_id
        return super().get_queryset().filter(company_id=company_id)
    
class CompanyDetail(generics.RetrieveUpdateAPIView):
    name = 'company-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CompanySerializer

    def get_object(self): # Sobrescreve o método get_object para retornar a Company à qual o usuário pertence.
        return self.request.user.company
    