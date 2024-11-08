from django.core.management.base import BaseCommand
from site_cc.models import Comentario  # Substitua 'your_app' pelo nome correto da sua aplicação

class Command(BaseCommand):
    help = 'Apaga todos os comentários existentes no banco de dados'

    def handle(self, *args, **kwargs):
        # Apagar todos os comentários
        Comentario.objects.all().delete()
        
        # Exibir mensagem de sucesso no terminal
        self.stdout.write("\033[91mTodos os comentarios foram apagados com sucesso!\033[0m")
