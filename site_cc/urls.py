from django.urls import path
from . import views
from .views import (
    clubes_view, 
    club_detail_view,
    CategoriaView,
    add_club_view,
    clube_update_view,
    delete_club_view,
    add_categoria_view,
    meus_clubes_view,
    aprovar_membro,
    adicionar_membro,
    recusar_membro,
    adicionar_membro_publico,
    avaliacao_view,
    add_comentario_view,
)

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('clube/<int:pk>/', club_detail_view, name='club-Detail'),
    path('addClube/', add_club_view, name='addClube'),
    path('clube/edit/<int:pk>/', clube_update_view, name='updateClube'),
    path('clube/delete/<int:pk>/', delete_club_view, name='deleteClube'),
    path('clubs/', clubes_view, name='clubs'),
    path('addCategoria/', add_categoria_view, name='addCategoria'),
    path('myclubes/',  meus_clubes_view, name='myclubes'),
    path('clube/<int:clube_id>/adicionar/', adicionar_membro, name='adicionar-membro'),
    path('clube/<int:clube_id>/aprovar/<int:membro_id>/', aprovar_membro, name='aprovar-membro'),
    path('clube/<int:clube_id>/recusar-membro/<int:membro_id>/', recusar_membro, name='recusar-membro'),
    path('categoria/<str:cats>/', CategoriaView, name='categoria'),
    path('clube/<int:clube_id>/juntar', adicionar_membro_publico, name='adicionar-membro-publico'),
    path('avaliacao/<int:pk>/', avaliacao_view, name='avaliacoes_clube'),
    path('clube/<int:pk>/Comentario/', add_comentario_view, name='add_comentario'),
    path('introducao/', views.introducao, name='introducao'),
    path('equipe/', views.equipe, name='equipe'),
    path('contato/', views.contato, name='contato'),
    path('clube/<int:clube_id>/atualizar_progresso/',views.atualizar_progresso, name='atualizar_progresso'),

]