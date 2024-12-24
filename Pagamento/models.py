from django.db import models

# Modelo de pagamento, porem não é utilizado no projeto por enquanto
class Pagamento(models.Model):
    nome = models.CharField(max_length=256)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    observacao = models.TextField()
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.valor} - {self.data}'