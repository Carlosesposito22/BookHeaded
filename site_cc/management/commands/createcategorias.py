from django.core.management.base import BaseCommand
from site_cc.models import Categoria  # Substitua 'site_cc' pelo nome da sua aplicação

class Command(BaseCommand):
    help = 'Cria categorias no banco de dados'

    def handle(self, *args, **kwargs):
        # Lista de categorias a serem criadas
        categorias = [
            "Ficção", "Não-ficção", "Fantasia", 
            "Biografia", "História", "Mistério", 
            "Romance", "Ciência", "Tecnologia", "Autoajuda"
        ]

        # Criar categorias no banco de dados
        for nome in categorias:
            Categoria.objects.create(nome=nome)

        # Exibir mensagem final de sucesso
        self.stdout.write("\033[92mTodas as categorias foram criadas com sucesso!\033[0m")