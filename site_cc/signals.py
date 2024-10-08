from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria, Modalidade

@receiver(post_migrate)
def create_categories_and_modalities(sender, **kwargs):
    if sender.name == 'site_cc':  
        categorias = [
            "Ficção", "Não-ficção", "Fantasia", 
            "Biografia", "História", "Mistério", 
            "Romance", "Ciência", "Tecnologia", "Autoajuda"
        ]
        modalidades = [
            "Online", "presencial", 
            "Hibrid"
        ]
        
        for categoria in categorias:
            Categoria.objects.get_or_create(nome=categoria)

        for modalidade in modalidades:
            Modalidade.objects.get_or_create(nome=modalidade)
