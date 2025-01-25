from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from User.models import perfilUsuario
from allauth.account.signals import user_signed_up


@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        perfilUsuario.objects.create(usuario=instance)


@receiver(user_signed_up)
def populate_email_on_signup(sender, request, user, **kwargs):
    """
    Preenche o campo email no perfilUsuario após cadastro via login social.
    """
    # Verifica se o usuário é do tipo perfilUsuario
    if isinstance(user, perfilUsuario):
        # Pega o email da conta social conectada
        social_account = user.socialaccount_set.first()
        if social_account:
            email = social_account.extra_data.get('email', '')
            if email and not user.email:  # Apenas atualiza se o email estiver vazio
                user.email = email
                user.save()
