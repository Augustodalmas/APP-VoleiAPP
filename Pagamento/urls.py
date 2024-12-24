from django.urls import path
from Pagamento.views import criar_sessao_stripe, pagina_sucesso, pagina_cancelado
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('checkout', criar_sessao_stripe, name='checkout'),
    path('sucesso', pagina_sucesso, name='sucesso'),
    path('cancelado', pagina_cancelado, name='cancelado'),
]
