from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login

from .models import *
from .serializers import *


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# class Auth(ModelViewSet):
#     model = User
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer
#
#     @action(methods=['post'], detail=False)
#     def login(self, request):
#         # print(MyTokenObtainPairSerializer.get_token('test'))
#         username = request.data["username"]
#         password = request.data["password"]
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return MyTokenObtainPairSerializer.get_token(user)
#         else:
#             Response('invalid login')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# class UsersViewSet(ModelViewSet):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer
#     # tokens.Token.for_user()
#     permission_classes = [permissions.IsAuthenticated]
#
#     @action(methods=['get'], detail=False)
#     def get(self, request):
#         users = Users.objects.all()
#         serializer = UsersSerializer(data=request.data, many = True)
#         serializer.is_valid()
#         return Response({'posts': users.data})
#
#     @action(methods=['post'], detail=False)
#     def post(self, request):
#         serializer = UsersSerializer(data=request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response({'users': serializer.data})


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, *args, **kwargs):
    #     pk = kwargs.get("pk", None)
    #     if not pk:
    #         return Response({"error": "Method PUT not allowed"})
    #
    #     try:
    #         # конкретная запись в таблице
    #         instance = about_user.objects.get(pk=pk)
    #     except:
    #         return Response({"error": "Method PUT not allowed"})
    #
    #     serializer = AboutUserSerializer(data=request.data, instance=instance)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({"posts": serializer.data})


class AboutUserAPIList(generics.ListCreateAPIView):
    queryset = About_user.objects.all()
    serializer_class = AboutUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # pagination_class = WomenAPIListPagination


class AboutUserAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = About_user.objects.all()
    serializer_class = AboutUserSerializer
    permission_classes = (IsAuthenticated, )


class UserProductAPIView(APIView):
    def get(self, request):
        products = User_product.objects.filter(user=request.user)
        return Response({'products': UserProductSerializer(products, many=True).data})

    # def post(self, request):
    #     data = request.data.copy()
    #     user = request.user
    #     data_product = request.data['name_product']
    #     print(data_product)
    #     coincidental_product = product.objects.get(name_product=data_product)
    #     print(coincidental_product)
    #     print(coincidental_product.pk)
    #     data['product'] = coincidental_product.pk
    #     data['user'] = user
    #     print(data)
    #     serializer = UserProductSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({'post': serializer.data})
    def post(self, request):
        data = request.data.copy()
        user = request.user
        if not len(User_product.objects.filter(name_product=data['name_product'])):
            original_product = Product.safe_get(Product, data['name_product'])
            if original_product is not None:
                new_user_product = User_product.objects.create(
                    name_product=data['name_product'],
                    total_count= data['total_count'],
                    calories=data['calories'],
                    user=user,
                    product=original_product
                )
                serializer = UserProductSerializer(new_user_product)
                return Response({'post': serializer.data})
            new_user_product = User_product.objects.create(
                name_product=data['name_product'],
                total_count=data['total_count'],
                calories=data['calories'],
                user=user,
                product=None
            )
            serializer = UserProductSerializer(new_user_product)
            return Response({'post': serializer.data})
        else:
            return Response({'Attention': 'Tne product has already been added '})

    def patch(self, request, *args, **kwargs):
        id_ingredient = kwargs.get("id", None)

        if not id_ingredient:
            return Response({"error": "Method PUT not allowed, not id_ingredient"})

        try:
            # конкретная запись в таблице
            instance = User_product.objects.get(pk=id_ingredient)
        except:
            return Response({"error": "Method PUT not allowed"})

        updated_user_product = UserProductSerializer().update(validated_data=request.data, instance=instance)
        return Response({"posts": UserProductSerializer(updated_user_product).data})

    def delete(self, request, **kwargs):
        id_ingredient = kwargs.get("id", None)
        try:
            # конкретная запись в таблице
            instance = User_product.objects.get(pk=id_ingredient)
        except:
            return Response({"error": "No post yet"})
        instance.delete()
        return Response("complete")


class UserRecipeAPIView(APIView):
    def get(self, request):
        recipes_for_user = []
        dictionary = {}
        products = User_product.objects.filter(user=request.user)
        for p in products:
            # get products from m2m products table
            try:
                true_product = Product.objects.get(user_product=p)
                recipes_p = Recipe.objects.filter(product=true_product)
                for r in recipes_p:
                    if r.title in dictionary:
                        dictionary[r.title]['count'] += 1
                    else:
                        dictionary[r.title] = {
                            "recipe": RecipeSerializer(r).data,
                            "count": 1
                        }

                    recipes_for_user.append(RecipeSerializer(r).data)
            except ObjectDoesNotExist:
                pass
        return Response({'products': dict})

