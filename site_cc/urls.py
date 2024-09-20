from django.urls import path
from .import views
from .views import clubesView, ClubDetailView, AddClubView, UpdateClubView, DeleteClubView,AddCategoriaView,meusclubesDetailView

urlpatterns = [
    path('',views.pagina_principal, name='pagina_principal'),
    path('about/', views.about, name='about'),
    path('login/',views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('clube/<int:pk>', ClubDetailView.as_view(), name="club-Detail"),
    path('addClube', AddClubView.as_view(), name="addClube"),
    path('clube/edit/<int:pk>', UpdateClubView.as_view(), name="updateClube"),
    path('clube/delete/<int:pk>', DeleteClubView.as_view(), name="deleteClube"),
    path('clubes/', clubesView.as_view(), name='clubes'),
    path('addCategoria', AddCategoriaView.as_view(), name="addCategoria"),
    path('meus_clubes/', meusclubesDetailView.as_view(), name='meus_clubes'),
   
]
