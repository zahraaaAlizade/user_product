from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import User, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'creator', 'created']
        read_only_fields = ['id', 'creator', 'created']


class UserAlreadyExist(APIException):
    status_code = 403
    default_detail = 'user with this username already exists.'
    default_code = 'service_unavailable'


class NotValidPassword(APIException):
    status_code = 400
    default_detail = 'Password must contain at least one special character (!, #, %, $, etc.)'
    default_code = 'service_unavailable'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):

        # Check if username already exists

        if User.objects.filter(username=value).exists():
            raise UserAlreadyExist

        # Check if username contains only alphabetic characters

        if not value.isalpha():
            raise serializers.ValidationError('Username must only contain alphabetic characters')

        return value

    def validate_password(self, value):

        # Check password length

        if len(value) < 8:
            raise serializers.ValidationError('Password length must be at least 8 characters')

        # Check if password contains at least one special character

        if not any(char in value for char in ['!', '#', '%', '$']):
            raise NotValidPassword

        return value

    def create(self, validated_data):

        # Hash password

        validated_data['password'] = make_password(validated_data['password'])
        validated_data['password'] = make_password(validated_data['password'])

        # Create user

        user = User.objects.create(**validated_data)

        return user
