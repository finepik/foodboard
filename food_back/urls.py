from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('about_user/', AboutUserAPIList.as_view()),
    path('about_user/update/<int:pk>/', AboutUserAPIUpdate.as_view()),
    path('user_product/', UserProductAPIView.as_view()),
    path('user_product/<int:id>/', UserProductAPIView.as_view()),
    path('user_product/update/<int:pk>/', UserProductAPIView.as_view()),
    path('user_product/delete/<int:pk>/', UserProductAPIView.as_view()),
    path('recipe/', UserRecipeAPIView.as_view()),
]