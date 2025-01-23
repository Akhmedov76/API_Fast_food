from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from app_foods.models import UserModel
from app_foods.serializers import RegisterSerializer, LoginSerializer


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
