from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import authentication, permissions, generics, routers
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User, State
from rest_framework.decorators import action
from .serializers import MyTokenObtainPairSerializer #追加
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from django.views import generic
# from django.views.generic import RetrieveAPIView
from accounts import permissions



# # ユーザ作成のView(POST)
# class AuthRegister(CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     @transaction.atomic
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # ユーザ情報取得のView(GET)
# class AuthInfoGetView(RetrieveAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get(self, request, format=None):
#         return Response(data={
#             'username': request.user.username,
#             'email': request.user.email,
#             },
#             status=status.HTTP_200_OK)

# # ユーザ情報更新のView(PUT)
# class AuthInfoUpdateView(UpdateAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserSerializer
#     lookup_field = 'email'
#     queryset = User.objects.all()

#     def get_object(self):
#         try:
#             instance = self.queryset.get(email=self.request.user)
#             return instance
#         except User.DoesNotExist:
#             raise Http404

# # ユーザ削除のView(DELETE)
# class AuthInfoDeleteView(DestroyAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserSerializer
#     lookup_field = 'email'
#     queryset = User.objects.all()

#     def get_object(self):
#         try:
#             instance = self.queryset.get(email=self.request.user)
#             return instance
#         except User.DoesNotExist:
#             raise Http404





class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.UpdateOwnProfile,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

#追加
# トークン（ユーザー情報）を取得するのに必要なView
class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyPageView(generics.RetrieveAPIView):
    permission_classes = (permissions.UpdateOwnProfile,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, format=None):

        return Response(data={
            'username': request.user.username,
            'email': request.user.email,
            'id': request.user.id,
            'password': request.user.password,
            'state': request.user.state,
            'city': request.user.city,
            'address': request.user.address,
            'zipcode': request.user.zipcode,
            'phone_number': request.user.phone_number,
            },
            status=status.HTTP_200_OK)