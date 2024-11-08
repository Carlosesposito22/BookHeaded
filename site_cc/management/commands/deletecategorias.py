from django.core.management.base import BaseCommand
from site_cc.models import Categoria  # Substitua 'your_app' pelo nome real da sua aplicação

class Command(BaseCommand):
    help = 'Apaga todas as categorias existentes no banco de dados'

    def handle(self, *args, **kwargs):
        # Apagar todas as categorias
        Categoria.objects.all().delete()
        
        # Exibir mensagem de sucesso no terminal
        self.stdout.write("\033[91mTodas as categorias foram apagadas com sucesso.\033[0m")