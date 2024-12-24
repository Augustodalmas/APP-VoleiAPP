import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from Partida.models import Partida
from django.shortcuts import render
from Notificacao.views import enviaEmailPagamento


# Configuração da API do Stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# Função para criar um produto no Stripe


def criar_produto_stripe(nome, preco):
    try:
        produto = stripe.Product.create(  # Cria o ID do produto na plataforma Stripe
            name=nome,
        )
        preco_obj = stripe.Price.create(  # Cria o preco do produto na plataforma Stripe
            product=produto.id,
            unit_amount=int(float(preco) * 100),
            currency="usd",
        )
        return produto.id, preco_obj.id
    except stripe.error.StripeError as e:
        raise Exception(f"Erro ao criar produto no Stripe: {str(e)}")


def criar_sessao_stripe(request, produto_id):
    partida = get_object_or_404(Partida, id=produto_id)
    try:
        sessao = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": partida.preco_stripe,
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=f'http://127.0.0.1:8000/partidas/{partida.id}/participar',
            cancel_url='http://127.0.0.1:8000/pagamento/cancelado',
        )
        return redirect(sessao.url)
    except stripe.error.StripeError as e:
        raise Exception(f"Erro ao criar sessão no Stripe: {str(e)}")


def pagina_sucesso(request):
    return render(request, 'sucesso.html')


def pagina_cancelado(request):
    return render(request, 'cancelado.html')
