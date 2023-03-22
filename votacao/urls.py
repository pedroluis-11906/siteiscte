from django.urls import path
from . import views
app_name = 'votacao'
urlpatterns = [
    # ex: votacao
    path('', views.index, name='index'),
    # ex: votacao/1
    path('<int:questao_id>', views.detalhe, name='detalhe'),
    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),
    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto, name='voto'),
    # ex: votacao/criarquestao
    path('criarquestao', views.criarquestao, name='criarquestao'),
    # ex: votacao/criarquestao/inserirquestao
    path('criarquestao/inserirquestao', views.inserirquestao, name='inserirquestao'),
    # ex votacao/2/criaropcao
    path('<int:questao_id>/criaropcao', views.criaropcao, name='criaropcao'),
    # ex votacao/2/criaropcao/inseriropcao
    path('<int:questao_id>/criaropcao/inseriropcao', views.inseriropcao, name='inseriropcao'),

    path('fazlogin', views.fazlogin, name='fazlogin'),
    path('fazlogout', views.fazlogout, name='fazlogout'),

    #ex votacao/registar
    path('registar', views.registar, name='registar'),

    #ex votacao/verperfil
    path('verperfil', views.verperfil, name='verperfil'),

    #ex votacao/6/apagaropcao
    path('<int:questao_id>/apagaropcao', views.apagaropcao, name='apagaropcao'),
]

