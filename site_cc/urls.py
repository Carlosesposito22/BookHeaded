from django.urls import path
from . import views
from .views import (
    clubesView, 
    ClubDetailView,
    CategoriaView,
    AddClubView,
    UpdateClubView,
    DeleteClubView,
    AddCategoriaView,
    meusclubesDetailView,
    aprovar_membro,
    adicionar_membro,
    recusar_membro,
    adicionar_membro_publico,
    AvaliacaoView,
    AddComentarioView,
)


urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('clube/<int:pk>/', ClubDetailView.as_view(), name='club-Detail'),
    path('addClube/', AddClubView.as_view(), name='addClube'),
    path('clube/edit/<int:pk>/', UpdateClubView.as_view(), name='updateClube'),
    path('clube/delete/<int:pk>/', DeleteClubView.as_view(), name='deleteClube'),
    path('clubs/', clubesView.as_view(), name='clubs'),
    path('addCategoria/', AddCategoriaView.as_view(), name='addCategoria'),
    path('myclubes/', meusclubesDetailView.as_view(), name='myclubes'),
    path('clube/<int:clube_id>/adicionar/', adicionar_membro, name='adicionar-membro'),
    path('clube/<int:clube_id>/aprovar/<int:membro_id>/', aprovar_membro, name='aprovar-membro'),
    path('clube/<int:clube_id>/recusar-membro/<int:membro_id>/', recusar_membro, name='recusar-membro'),
    path('categoria/<str:cats>/', CategoriaView, name='categoria'),
    path('clube/<int:clube_id>/juntar', adicionar_membro_publico, name='adicionar-membro-publico'),
    path('avaliacao/<int:pk>/', AvaliacaoView, name='avaliacoes_clube'),
    path('clube/<int:pk>/Comentario/', AddComentarioView.as_view(), name='add_comentario'),
]
