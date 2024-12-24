from django.urls import path, include
from User.views import carregar_cidades, ranking


urlpatterns = [
    path('cidades/', carregar_cidades, name='Carregar-cidades'),
    path('ranking/', ranking, name='ranking')
]
