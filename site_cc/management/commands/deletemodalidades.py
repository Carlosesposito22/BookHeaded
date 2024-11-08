from django.core.management.base import BaseCommand
from site_cc.models import Modalidade  # Substitua 'site_cc' pelo nome da sua aplicação

class Command(BaseCommand):
    help = 'Apaga todas as modalidades existentes no banco de dados'

    def handle(self, *args, **kwargs):
        # Apagar todas as modalidades
        Modalidade.objects.all().delete()
        
        # Exibir mensagem de sucesso no terminal
        self.stdout.write("\033[91mTodas as modalidades foram apagadas com sucesso!\033[0m")
