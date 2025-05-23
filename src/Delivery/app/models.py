from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def esta_ativo(self):
        """RN04: Verifica se a conta está ativa"""
        return self.ativo and (timezone.now() - self.data_cadastro) < timezone.timedelta(days=365)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cpf'], name='cpf_unico')
        ]

class Restaurante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=18, unique=True)
    aprovado = models.BooleanField(default=False)  # RN02
    avaliacao_media = models.FloatField(default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    destaque = models.BooleanField(default=False)  # RN07
    raio_entrega = models.IntegerField(default=15)  # RN05 em km
    
    def pode_entregar(self, distancia):
        """RN05: Verifica se o restaurante atende a localização"""
        return distancia <= self.raio_entrega

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ACEITO', 'Aceito pelo restaurante'),
        ('PREPARO', 'Em preparo'),
        ('ENTREGA', 'Saiu para entrega'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    data_pedido = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    taxa_entrega = models.DecimalField(max_digits=10, decimal_places=2)
    
    def pode_ser_cancelado(self):
        """RN08: Verifica se o pedido ainda pode ser cancelado"""
        return (self.status in ['PENDENTE', 'ACEITO'] and 
                (timezone.now() - self.data_pedido) < timezone.timedelta(minutes=5))
    
    def calcular_taxa(self):
        """RN10: Calcula taxa adicional para pedidos pequenos"""
        if self.valor_total < 15:
            self.taxa_entrega += 5.00