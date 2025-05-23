from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import PedidoSerializer
from .models import Cliente, Restaurante, Pedido

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
    #def create(self, request, *args, **kwargs):
     # RN05: Verifica distância do restaurante
     #   cliente = request.user.cliente
     #   restaurante = Restaurante.objects.get(pk=request.data['restaurante'])
        #distancia = calcular_distancia(cliente.endereco, restaurante.endereco)
        
     #if not restaurante.pode_entregar(distancia):
     #    return Response(
     #        {"detail": "Restaurante não atende sua localização"},
     #        status=status.HTTP_400_BAD_REQUEST
     #    )
        
     #   return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # RN08: Permite cancelamento apenas no período permitido
        instance = self.get_object()
        if not instance.pode_ser_cancelado():
            return Response(
                {"detail": "Pedido não pode mais ser cancelado"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)