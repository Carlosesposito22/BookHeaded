from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Apaga todos os usuários criados'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Todos os usuários foram apagados com sucesso.'))