from rest_framework.routers import SimpleRouter
from .views import AuthViewSet

app_name = "auth"
router = SimpleRouter()
router.register('Auth', AuthViewSet, basename='auth')

urlpatterns = [

    *router.urls,
]
