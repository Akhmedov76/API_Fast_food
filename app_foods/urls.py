from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import AuthViewSet, UserViewSet, MenuItemViewSet, OrderViewSet, OrderItemViewSet

app_name = "auth"

router = SimpleRouter()
# router = DefaultRouter()
router.register('Auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet)
router.register('menu-items', MenuItemViewSet)
router.register('orders', OrderViewSet)
router.register('order-items', OrderItemViewSet)
urlpatterns = [

    *router.urls,
]
