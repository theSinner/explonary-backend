from rest_framework import serializers
from .models import User


class RequestUserAuthPost(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RequestUserAuthPut(serializers.Serializer):
    fullname = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)


class RequestUserItemGet(serializers.Serializer):
    username = serializers.CharField(required=True)


class RequestUserActivateRequestPost(serializers.Serializer):
    field = serializers.CharField(required=False, default='email')


class RequestUserActivateConfirmPut(serializers.Serializer):
    field = serializers.CharField(required=False, default='email')
    code = serializers.CharField(required=True)


class RequestUserEditPut(serializers.Serializer):
    fullname = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)


class ResponseProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ResponseUserDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'avatar',
            'full_name'
        ]
