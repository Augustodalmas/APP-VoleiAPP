from django.db import models
from User.models import perfilUsuario
from django.core.files.base import ContentFile
from django.utils import timezone
import qrcode
from io import BytesIO


class Local(models.Model):
    nome = models.CharField(max_length=256)
    cidade = models.CharField(max_length=256)
    bairro = models.CharField(max_length=256)
    rua = models.CharField(max_length=256)
    numero = models.IntegerField()
    CEP = models.CharField(max_length=9)

    def __str__(self):
        return self.nome


class Partida(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
# Amador - profissional
    INICIANTE = 'Iniciante'
    INTERMEDIARIO = 'Intermediário'
    AVANCADO = 'Avançado'
    NIVEL = [
        (INICIANTE, 'Iniciante'),
        (INTERMEDIARIO, 'Intermediário'),
        (AVANCADO, 'Avançado'),
    ]
    nivel = models.CharField(max_length=15, choices=NIVEL, default=INICIANTE)

    CINCOX1 = '5x1'
    SEISX0 = '6x0'
    QUATROX2 = '4x2'
    ROTACAO = [
        (CINCOX1, '5x1'),
        (SEISX0, '6x0'),
        (QUATROX2, '4x2'),
    ]
    rotacao = models.CharField(max_length=3, choices=ROTACAO, default=SEISX0)
    data = models.DateField()
    hora = models.TimeField()
    local = models.ForeignKey(
        Local, on_delete=models.PROTECT, related_name="Quadra_jogo")
    organizador = models.ForeignKey(perfilUsuario, on_delete=models.CASCADE)
    lotacao = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    # Adicionado itens de Pagamento
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    id_stripe = models.CharField(max_length=256, blank=True, null=True)
    preco_stripe = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['data', 'hora', 'local'], name='unique_partida')
        ]

    def gerar_qr_code(self):
        qr_data = f"https://augustodalmas.pythonanywhere.com/partidas/{self.id}/checkin"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer)
        self.qr_code.save(f'partida_{self.id}.png', ContentFile(
            buffer.getvalue()), save=False)
        buffer.close()
        self.save()

    def __str__(self):
        return self.titulo


class Participacao(models.Model):
    usuario = models.ForeignKey(perfilUsuario, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    pago = models.BooleanField(default=False)
    check_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'partida'], name='unique_participacao')
        ]

    def realizar_check_in(self):
        self.check_in = True
        self.check_in_time = timezone.now()
        self.save()


class HistoricoPartida(models.Model):
    partida = models.ForeignKey(
        Partida,
        on_delete=models.CASCADE,
        related_name='historicos'
    )
    data = models.DateField()
    participacao = models.BooleanField(default=False)
