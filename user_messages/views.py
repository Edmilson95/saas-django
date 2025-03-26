from rest_framework import permissions
from rest_framework import generics

from . import serializers
from .models import UserMessage

class UserMessageList(generics.ListCreateAPIView):
    name = 'usermessage-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserMessageSerializer
    queryset = UserMessage.objects.all()

    def perform_create(self, serializer): # garante que a UserMessage esteja relacionada à empresa à qual o usuário logado pertence.
        user = self.request.user
        company_id = user.company_id
        serializer.save(company_id=company_id, from_user=user)

    def get_queryset(self):
        return UserMessage.objects.get_for_user(self.request.user)
    
class UserMessageDetail(generics.RetrieveAPIView): # estende a classe generics.RetrieveAPIView. Isso significa que uma UserMessage não pode ser editada ou excluída (só pode ser visualizada).
    name = 'usermessage-detail'
    permission_classes = (
        permissions.IsAuthenticated
    )
    serializer_class = serializers.UserMessageSerializer

    def get_queryset(self):
        return UserMessage.objects.get_for_user(self.request.user)

