from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
# from food_back.models import User
from django.contrib.auth.models import User

from .models import *


# class UsersSerializer(serializers.Serializer):
#     user_name = serializers.CharField(max_length=80)
#     email = serializers.CharField(max_length=80)
#     password = serializers.CharField(max_length=30)
#     avatar = serializers.ImageField()
#
#     def create(self, validated_data):
#         return Users.objects.create(**validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):


    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token

class AboutUserSerializer(serializers.ModelSerializer):
    # сохранение текущего пользователя в скрытом поле, отображается при добавлении записи
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = About_user
        fields = "__all__"



class UserProductSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = User_product
        fields = "__all__"

    def update(self, instance, validated_data):
        print('update ALARM ALLARM')
        instance.name_product = validated_data.get('name_product', instance.name_product)
        instance.total_count = validated_data.get('total_count', instance.total_count)
        instance.calories = validated_data.get('calories', instance.calories)
        instance.user = validated_data.get('user', instance.user)
        instance.product = validated_data.get('product', instance.product)
        instance.save()
        return instance


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"


