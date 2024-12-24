from django.db import models
from django.contrib.auth.models import AbstractUser


class Cidade(models.Model):
    nome = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome} - {self.estado}"


class perfilUsuario(AbstractUser):
    data_nascimento = models.DateField(blank=True, null=True)
    numero_telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True)
    cidade = models.ForeignKey(
        Cidade, on_delete=models.CASCADE, default=4702)
    LEV = 'Levantador'
    OP = 'Oposto'
    CEN = 'Central'
    LIB = 'Libero'
    PON = 'Ponteiro'
    POSICOES = [
        (LEV, 'Levantador'),
        (OP, 'Oposto'),
        (CEN, 'Central'),
        (LIB, 'Libero'),
        (PON, 'Ponteiro'),
    ]
    posicao = models.CharField(max_length=12, choices=POSICOES)
    INICIANTE = 'Iniciante'
    INTERMEDIARIO = 'Intermediario'
    AVANCADO = 'Avancado'
    NIVEL = [
        (INICIANTE, 'Iniciante'),
        (INTERMEDIARIO, 'Intermediario'),
        (AVANCADO, 'Avancado'),
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
    pontuacao = models.IntegerField(default=0)
    foto = models.ImageField(
        upload_to="perfil_imagens/", blank=True, null=True)
    historicos = models.ManyToManyField(
        'Partida.HistoricoPartida',  # Nome do modelo em formato string
        related_name='usuarios',
        blank=True
    )

    def __str__(self):
        return self.username
