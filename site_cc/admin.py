from django.contrib import admin
from .models import Clube, Categoria, Modalidade, Comentario

admin.site.register(Clube)
admin.site.register(Categoria)
admin.site.register(Modalidade)
admin.site.register(Comentario)
