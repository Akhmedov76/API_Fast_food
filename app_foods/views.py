from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from app_foods.models import UserModel, MenuItemModel, OrderModel, OrderItemModel
from app_foods.serializers import RegisterSerializer, LoginSerializer, UserSerializer, MenuItemSerializer, \
    OrderSerializer, OrderItemSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class UserViewSet(APIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class MenuItemViewSet(APIView):
    queryset = MenuItemModel.objects.all()
    serializer_class = MenuItemSerializer


class OrderViewSet(APIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(APIView):
    queryset = OrderItemModel.objects.all()
    serializer_class = OrderItemSerializer
