from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from core.models import CompanyRelatedModel

User = get_user_model()

class UserMessageManager(models.Manager):

    def get_for_user(self, user):
        # Esse método primeiro filtra pelo company_id para garantir que nada de outras empresas seja retornado. 
        # Em seguida, ele filtra as mensagens enviadas por ou para o usuário passado como argumento.
        return self.all().filter(company_id=user.company_id).filter(Q(from_user=user) | Q(to_user=user))    


class UserMessage(CompanyRelatedModel):
    # id: Este campo vem do CompanyRelatedModel.
    # company: Este campo também vem do CompanyRelatedModel. Ele relaciona uma mensagem de usuário a uma empresa.
    text = models.TextField('message', blank=False, null=False)
    date = models.DateTimeField('date', auto_now_add=True)
    from_user = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_messages'
        ordering = ['date']