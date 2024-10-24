from django.core.management.base import BaseCommand
from site_cc.models import Modalidade  # Substitua 'site_cc' pelo nome da sua aplicação

class Command(BaseCommand):
    help = 'Cria modalidades no banco de dados'

    def handle(self, *args, **kwargs):
        # Lista de modalidades a serem criadas
        modalidades = [
            "online",
            "presencial",
            
        ]

        # Criar modalidades no banco de dados
        for nome in modalidades:
            Modalidade.objects.create(nome=nome)
            self.stdout.write(self.style.SUCCESS(f'Modalidade "{nome}" criada com sucesso.'))

        # Exibir mensagem final de sucesso
        self.stdout.write(self.style.SUCCESS('Todas as modalidades foram criadas com sucesso.'))