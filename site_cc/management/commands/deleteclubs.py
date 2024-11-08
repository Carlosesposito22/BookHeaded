from django.core.management.base import BaseCommand
from site_cc.models import Clube  # Substitua 'your_app' pelo nome real da sua aplicação

class Command(BaseCommand):
    help = 'Apaga todos os clubes existentes no banco de dados'

    def handle(self, *args, **kwargs):
        # Apagar todos os clubes
        Clube.objects.all().delete()
        
        # Exibir mensagem de sucesso no terminal
        self.stdout.write("\033[91mTodos os clubes foram apagados com sucesso!\033[0m")
