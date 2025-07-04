from django.urls import path
from Partida.views import criarPartida, listaPartida, verPartida, exibirQRCodeView, realizarCheckInView, entrarPartida, minhasPartidas, meuHistorico, AdicionarLocal


urlpatterns = [
    path('', listaPartida.as_view(), name='ListaPartidas'),
    path('criar/', criarPartida.as_view(), name='criarPartida'),
    path('<int:pk>', verPartida.as_view(), name='verPartida'),
    path('<int:pk>/qr_code', exibirQRCodeView.as_view(), name='exibir_qr_code'),
    path('<int:partida_id>/checkin',
         realizarCheckInView.as_view(), name='realizar_check_in'),
    path('<int:partida_id>/participar',
         entrarPartida.as_view(), name='entrar_partida'),
    path('minhas_partidas',
         minhasPartidas.as_view(), name='minhas_partidas'),
    path('historico',
         meuHistorico.as_view(), name='historico'),
    #     path('<int:produto_id>/checkout', criar_sessao_stripe, name='checkout'),
    path('criar_local/', AdicionarLocal.as_view(), name="adicionar_local"),
]
