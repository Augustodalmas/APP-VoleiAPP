from django.core.mail import send_mail


class envioEmailParticipar:
    Assunto = "Notificação do voleiAPP"

    @staticmethod
    def enviar_email(user, partida):
        Mensagem = f"""
        Olá { user.username },

        Parabéns! Sua inscrição na partida "{ partida.titulo }" foi confirmada com sucesso.

        **Detalhes da Partida:**
        - **Data:** { partida.data }
        - **Horário:** { partida.hora }
        - **Local:** { partida.local }

        Prepare-se para se divertir e dar o seu melhor! Se tiver alguma dúvida, entre em contato conosco.

        Nos vemos em breve na quadra!
        Equipe VoleiAPP"""

        if not user.email:
            raise ValueError("Usuário não possui um email cadastrado.")

        send_mail(
            subject=envioEmailParticipar.Assunto,
            message=Mensagem,
            from_email='python.para.programacao@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )


class envioEmailCheckin:
    Assunto = "Notificação do voleiAPP"

    @staticmethod
    def enviar_email(user, partida):
        Mensagem = f"""
        Olá { user.username },  

        O check-in para a partida "{ partida.titulo }" foi realizado com sucesso!

        **Detalhes da Partida:**  
        - **Data:** { partida.data }
        - **Horário:** { partida.hora }
        - **Local:** { partida.local }

        Estamos felizes por saber que você está pronto para o jogo.

        Boa partida!
        Equipe VoleiAPP
        """
        if not user.email:
            raise ValueError("Usuário não possui um email cadastrado.")

        send_mail(
            subject=envioEmailCheckin.Assunto,
            message=Mensagem,
            from_email='python.para.programacao@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )


class envioEmailCriarPartida():
    Assunto = "Notificação do voleiAPP"

    @staticmethod
    def enviar_email(user, partida):
        Mensagem = f"""
        Olá {user.username},

        Sua partida "{ partida.titulo }" foi criada com sucesso no VoleiAPP!

        **Detalhes da Partida:**
        - **Data:** { partida.data }
        - **Horário:** { partida.hora }
        - **Local:** { partida.local }

        Agora é só convidar outros jogadores para participarem e se prepararem para um grande jogo.

        Qualquer dúvida, estamos à disposição!
        Equipe VoleiAPP  
        """
        if not user.email:
            raise ValueError("Usuário não possui um email cadastrado.")

        send_mail(
            subject=envioEmailCriarPartida.Assunto,
            message=Mensagem,
            from_email='python.para.programacao@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )


class enviaEmailPagamento():
    Assunto = "Notificação de pagamento do voleiAPP"

    @staticmethod
    def enviar_email(user, partida):
        Mensagem = f"""
        Olá {user.username},

        Sua partida "{ partida.titulo }" foi paga com sucesso o valor de {partida.valor}!

        **Detalhes da Partida:**
        - **Data:** { partida.data }
        - **Horário:** { partida.hora }
        - **Local:** { partida.local }

        Qualquer dúvida, estamos à disposição!
        Equipe VoleiAPP  
        """
        if not user.email:
            raise ValueError("Usuário não possui um email cadastrado.")

        send_mail(
            subject=envioEmailCriarPartida.Assunto,
            message=Mensagem,
            from_email='python.para.programacao@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
