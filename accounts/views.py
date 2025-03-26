from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from core.views import CompanySafeViewMixin
from . import serializers

User = get_user_model()

class AccountCreate(generics.CreateAPIView): # Herda de CreateAPIView, então não haverá como listar ou atualizar as contas.
    name = 'account-create'
    serializer_class = serializers.AccountSerializer

class UserList(CompanySafeViewMixin, generics.ListCreateAPIView):
    name = 'user-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    # Removido get_queryset e perform_create pois herdamos de CompanySafeViewMixin
    
class UserDetail(CompanySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    name = 'user-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    # Removido get_queryset pois herdamos de CompanySafeViewMixin

class CompanyDetail(generics.RetrieveUpdateAPIView):
    name = 'company-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CompanySerializer

    def get_object(self): # Sobrescreve o método get_object para retornar a Company à qual o usuário pertence.
        return self.request.user.company
    