from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, get_distance

router = DefaultRouter()
router.register('orders', OrderViewSet)
router.register('order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('get-distance/', get_distance, name="get-distance"),
]
