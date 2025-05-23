# Exemplo de validações em serializers.py
import datetime
from django.utils import timezone
from rest_framework import serializers
from .models import Cliente, Restaurante, Pedido, Pagamento
from rest_framework import serializers
from django.core.exceptions import ValidationError

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
    
    def validate(self, data):
        # RN09: Verifica se o restaurante está aberto
        if not data['restaurante'].aberto:
            raise serializers.ValidationError("Restaurante não está aberto no momento")
        
        # RN11: Valida observações extras
        itens = data.get('itens', [])
        for item in itens:
            if len(item.get('observacoes', '').split(',')) > 3:
                raise serializers.ValidationError("Máximo de 3 observações por item")
        
        return data

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'
    
    def validate(self, data):
        # RN13: Bloqueia após 3 tentativas falhas
        cliente = data['pedido'].cliente
        tentativas_falhas = Pagamento.objects.filter(
            pedido__cliente=cliente,
            status='RECUSADO',
            data__gte=timezone.now() - timezone.timedelta(hours=1)
        ).count()
        
        if tentativas_falhas >= 3:
            raise serializers.ValidationError("Muitas tentativas falhas. Conta temporariamente bloqueada.")
        
        return data