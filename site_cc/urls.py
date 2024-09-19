

from django.urls import path
from .import views


urlpatterns = [
    path('',views.pagina_principal, name='pagina_principal'),
    path('login/',views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
   
]
