from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.pagina_login, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('sair/', views.sair, name='sair'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editar/<int:id>/', views.editar_nota, name='editar_nota'),
    path('deletar/<int:id>/', views.deletar_nota, name='deletar_nota'),
]