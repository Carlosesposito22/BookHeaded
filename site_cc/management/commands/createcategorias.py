from django.core.management.base import BaseCommand
from site_cc.models import Categoria  # Substitua 'site_cc' pelo nome da sua aplicação

class Command(BaseCommand):
    help = 'Cria categorias no banco de dados'

    def handle(self, *args, **kwargs):
        # Lista de categorias a serem criadas
        categorias = [
            "Ficção",
            "Não-ficção",
            "Mistério",
            "Romance",
            "História",
            "Ciência",
            "Filosofia"
        ]

        # Criar categorias no banco de dados
        for nome in categorias:
            Categoria.objects.create(nome=nome)
            self.stdout.write(self.style.SUCCESS(f'Categoria "{nome}" criada com sucesso.'))

        # Exibir mensagem final de sucesso
        self.stdout.write(self.style.SUCCESS('Todas as categorias foram criadas com sucesso.'))