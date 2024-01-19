from rest_framework import serializers
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.hashers import make_password
from .models import MyUser, Myapp


class MyappSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myapp
        fields = [
            "id",
            "title",
        ]


class MyUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = MyUser
        fields = [
            "id",
            "username",
            "password",
        ]

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        auth_user = MyUser.objects.create(**validated_data)
        return auth_user


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            "id",
            "name",
            "content_type",
            "codename",
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "permissions",
        ]
