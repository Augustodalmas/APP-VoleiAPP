from django.views.generic import ListView, CreateView, DetailView, View
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from Partida.models import Partida, Participacao, HistoricoPartida
from User.models import perfilUsuario
from Pagamento.views import criar_produto_stripe
from Partida.forms import formPartida
from Notificacao.views import envioEmailParticipar, envioEmailCheckin, envioEmailCriarPartida, enviaEmailPagamento


class listaPartida(ListView):
    model = Partida
    template_name = 'principal.html'
    context_object_name = 'partidas'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['hoje'] = now().date()
        return contexto


class criarPartida(CreateView):
    model = Partida
    template_name = 'criar_partida.html'
    form_class = formPartida
    context_object_name = 'CriaPartida'
    success_url = reverse_lazy('ListaPartidas')

    def form_valid(self, form):
        form.instance.organizador = self.request.user
        response = super().form_valid(form)
        partida = self.object
        perfil_usuario = perfilUsuario.objects.get(
            username=self.request.user.username)  # Pega o usuario que está usando

        if partida.nivel == "Iniciante":
            partida.valor = 5
        elif partida.nivel == "Intermediario":
            partida.valor = 7
        elif partida.nivel == "Avancado":
            partida.valor = 9
        try:
            # Criar o produto junto com o Preço no Stripe
            stripe_produto_id, stripe_preco_id = criar_produto_stripe(
                nome=partida.titulo,
                preco=partida.valor,
            )
            partida.id_stripe = stripe_produto_id
            partida.preco_stripe = stripe_preco_id
            partida.save()
            #  Envia o email para o usuario que está logado
            envioEmailCriarPartida.enviar_email(perfil_usuario, partida)
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")  # Alterar
        return response


class verPartida(LoginRequiredMixin, DetailView):
    model = Partida
    template_name = 'ver_partida.html'
    context_object_name = 'verPartida'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['participacao'] = Participacao.objects.filter(
            usuario=self.request.user, partida=self.object
        ).first()
        return contexto


class exibirQRCodeView(DetailView):
    model = Partida
    template_name = 'partida_qr_code.html'
    context_object_name = 'partida'

    def get_object(self, queryset=None):
        partida = super().get_object(queryset)
        if not partida.qr_code:
            partida.gerar_qr_code()
        return partida

    def dispatch(self, request, *args, **kwargs):
        partida = get_object_or_404(Partida, id=self.kwargs['pk'])
        if partida.organizador != request.user:
            return render(request, "sem_acesso.html")
        return super().dispatch(request, *args, **kwargs)


class realizarCheckInView(LoginRequiredMixin, View):
    def get(self, request, partida_id, ):
        partida = get_object_or_404(Partida, id=partida_id)
        perfil_usuario = perfilUsuario.objects.get(
            username=request.user.username)
        mensagem = ''  # Mensagem padrão
        tipo_mensagem = ''  # Tipo padrão

        if now().date() != partida.data:  # Verificação da data, caso não seja mesmo dia, vai dar erro
            mensagem = 'Check-in permitido apenas no dia da partida.'
            tipo_mensagem = 'erro'
        else:
            participacao = Participacao.objects.filter(
                usuario=request.user, partida=partida
            ).first()  # Filtra se o usuario está participando da partida
            if not participacao:
                mensagem = 'Você não está inscrito nesta partida.'
                tipo_mensagem = 'erro'
            elif participacao.check_in:  # Caso já tenha checkin
                mensagem = 'Check-in já realizado.'
                tipo_mensagem = 'erro'
            else:
                try:
                    # Chama notificação para enviar o Email
                    envioEmailCheckin.enviar_email(perfil_usuario, partida)
                except Exception as e:
                    mensagem = f'Usuário realizou checkin com sucesso, mas ocorreu um erro ao enviar o email: {e}'
                    tipo_mensagem = 'erro'
                participacao.realizar_check_in()  # Realiza o checkin na partida
                mensagem = 'Check-in realizado com sucesso!'
                tipo_mensagem = 'sucesso'

                # Adiciona a partida ao Histórico do usuario
                historico = HistoricoPartida.objects.create(
                    partida=partida,
                    data=now(),
                    participacao=True
                )
                perfil_usuario.historicos.add(historico)

                # Adiciona a pontuação ao usuario
                if partida.nivel == "Iniciante":
                    perfil_usuario.pontuacao += 1
                    perfil_usuario.save()
                elif partida.nivel == 'Intermediario':
                    perfil_usuario.pontuacao += 2
                    perfil_usuario.save()
                else:
                    perfil_usuario.pontuacao += 3
                    perfil_usuario.save()

        return render(request, 'checkin.html', {
            'mensagem': mensagem,
            'tipo_mensagem': tipo_mensagem,
            'partida': partida,
        })


class entrarPartida(LoginRequiredMixin, View):
    def get(self, request, partida_id):
        partida = get_object_or_404(
            Partida, id=partida_id)  # pega o id da partida
        perfil_usuario = request.user  # pega o perfil do usuario
        participacao = Participacao.objects.filter(
            usuario=perfil_usuario, partida=partida
        ).first()  # Verifica a participação do usuario
        mensagem = ''  # mensagem padrão
        tipo_mensagem = ''  # tipo padrão

        if not participacao:
            participacao = Participacao(
                usuario=perfil_usuario, partida=partida)
            participacao.save()  # Se não participar, entrar na partida e salvar

            try:
                # Envia o Email de participação
                envioEmailParticipar.enviar_email(perfil_usuario, partida)
                enviaEmailPagamento.enviar_email(perfil_usuario, partida)
                participacao.pago = True  # Marca a partida como paga
                participacao.save()
                partida.lotacao -= 1  # Diminui a lotação da partida
                partida.save()

                mensagem = 'Usuário entrou na partida com sucesso!'
                tipo_mensagem = 'sucesso'
            except Exception as e:
                mensagem = f'Usuário entrou na partida, mas ocorreu um erro ao enviar o email: {e}'
                tipo_mensagem = 'erro'
                participacao.pago = True  # Marca a partida como paga
                participacao.save()
                partida.lotacao -= 1  # Diminui a lotação da partida
                partida.save()
        else:
            mensagem = 'Usuário já se encontra na partida!'
            tipo_mensagem = 'erro'

        return render(request, 'check_partida.html', {
            'mensagem': mensagem,
            'tipo_mensagem': tipo_mensagem,
            'partida': partida,
        })


class minhasPartidas(ListView):
    model = Partida
    template_name = 'minhas_partidas.html'
    context_object_name = 'partidas'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['hoje'] = now().date()
        return contexto

    def get_queryset(self):
        return Partida.objects.filter(
            participacao__usuario=self.request.user
        ).distinct()


class meuHistorico(ListView):
    model = Partida
    template_name = 'historico.html'
    context_object_name = 'partidas'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['hoje'] = now().date()
        contexto['hora'] = now().hour
        return contexto

    def get_queryset(self):
        return Partida.objects.filter(
            participacao__usuario=self.request.user
        ).distinct()
