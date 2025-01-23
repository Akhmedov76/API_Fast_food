from rest_framework import serializers
from .models import UserModel

UserChoice = [
    'admin', 'user', 'courier'
]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)
    username = serializers.CharField(max_length=150, required=True)
    role = serializers.ChoiceField(
        default=UserChoice[0],
        choices=UserChoice)

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'role', 'confirm_password']

    def validate(self, data):
        confirmed_password = data.pop('confirm_password')

        if data['password'] != confirmed_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords must match'})
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        user = UserModel.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            return data
        else:
            raise serializers.ValidationError({'username': 'Invalid credentials'})
