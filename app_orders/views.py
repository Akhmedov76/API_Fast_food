from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_orders.models import OrderModel, OrderItemModel
from app_orders.serializers import OrderSerializer, OrderItemSerializer
import geopy.distance


class OrderViewSet(ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        rest_distance = (41.34756202490278, 69.28407669659572)  # Restoran koordinatalari
        client_lat = float(self.request.data.get('lat'))
        client_lon = float(self.request.data.get('lon'))

        # Masofani hisoblashdelivery_address
        client_cords = (client_lat, client_lon)
        distance = geopy.distance.geodesic(rest_distance, client_cords).km

        print(f"Masofa: {distance:.2f} km")  # Faqat logga chiqaramiz, bazaga yozmaymiz

        serializer.save(user=self.request.user)


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItemModel.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def get_distance(request):
    rest_distance = ('41.34756202490278', '69.28407669659572')
    client_cords = (request.GET.get('lat'), request.GET.get('lon'))
    return Response({'message': geopy.distance.geodesic(rest_distance, client_cords).km})
