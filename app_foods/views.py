from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from app_foods.models import UserModel, MenuItemModel, OrderModel, OrderItemModel
from app_foods.serializers import RegisterSerializer, LoginSerializer, UserSerializer, MenuItemSerializer, \
    OrderSerializer, OrderItemSerializer


class AuthViewSet(ViewSet):
    """
    Bitta ViewSet ichida login va register endpointlari.
    """

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


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
