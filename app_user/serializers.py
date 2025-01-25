from openid.cryptutil import sha256
from rest_framework import serializers

from app_user.models import UserModel, UserStatusChoice

UserChoice = [
    'admin', 'user', 'waiter'
]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)
    username = serializers.CharField(max_length=150, required=True)
    role = serializers.ChoiceField(
        default=UserChoice[1],
        choices=UserChoice)

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'role', 'confirm_password']

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if data['password'] != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords must match'})
        return data

    def create(self, validated_data):
        user = UserModel(
            username=validated_data['username'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        response = {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'status': user.status,
        }
        return response


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        try:
            user = UserModel.objects.get(username=data['username'])
        except UserModel.DoesNotExist:
            raise serializers.ValidationError({'username': 'User not found'})

        if not user.check_password(data['password']):
            raise serializers.ValidationError({'password': 'Incorrect password'})

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'role', 'status']
