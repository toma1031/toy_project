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

from accounts import permissions
from rest_framework.permissions import IsAuthenticated



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
    # UpdateOwnProfileはUserViewで適用しているカスタムパーミッションです。UpdateOwnProfileにより、ユーザーは自身のプロフィールのみアップデートできるように制限をかけています。
    permission_classes = (permissions.UpdateOwnProfile,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Reactからのリクエストは文字列を想定しているためAPIコンソールでのアップデート時にはうまくいかないということです。つまり、APIコンソールからのアップデートではstateをオブジェクトで直接指定できるため、update()に記述しているようにリクエスト内のstateを文字列から処理する必要がありません。
    # 対して、Reactからのアップデートは文字列でリクエストを送信しているため、APIコンソールで動作する同じ環境ではpatchが上手く動きません。
    # APIコンソールからのアップデートは、UserViewSetのupdate()をコメントアウトすることでうまくいくと思います。

    # DRFでアップデートするときは下記をコメントアウトしないといけない、理由は上記の通り
    # 対してReactでアップデートするときは下記コードを有効にしておかなければならない
    # ですが
    # update()を追加した意味は、stateを文字列でリクエストした時に上手く動作させるためです。ですので、React側で数字でリクエストする仕様を採用する場合はModelViewSet標準のupdate()で機能できますので、追加したupdate()は必要ありません。
    # def update(self, request, pk, partial=True):
    #     user = request.user
    #     # 文字列で送信されているstateから，それに対応するstateオブジェクトを取得
    #     state = State.objects.get(state=request.data['state'])
    #     # 上記で取得したオブジェクトを指定
    #     data={'state':state.id}
    #     serializer = self.serializer_class(user, data=data, partial=True)
    #     if serializer.is_valid():
    #         print(serializer.is_valid)
    #         serializer.save()

#追加
# トークン（ユーザー情報）を取得するのに必要なView
class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyPageView(generics.RetrieveAPIView):
    # UpdateOwnProfileはUserViewで適用しているカスタムパーミッションです。UpdateOwnProfileにより、ユーザーは自身のプロフィールのみアップデートできるように制限をかけています。対して、MyPageViewではUserViewと異なり、アップデート処理を行わないので、認証ユーザーのみアクセス権を与えるisAuthenticatedの方が適していると思います。
    permission_classes = (IsAuthenticated,)
    # permission_classes = (permissions.UpdateOwnProfile,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        data = UserSerializer(user).data
        # DRFの MyPageViewでpasswordをしっかり返せているか確認してみてください。おそらく以前のままでしたら、MyPageViewでpasswordはrerurnしていないと思います。
        # return Response(data={
        #     'username': request.user.username,
        #     'email': request.user.email,
        #     'id': request.user.id,
        #     'password': request.user.password,
        #     'state': request.user.state,
        #     'city': request.user.city,
        #     'address': request.user.address,
        #     'zipcode': request.user.zipcode,
        #     'phone_number': request.user.phone_number,
        #     },
        #     status=status.HTTP_200_OK)

        # DRFの MyPageViewでpasswordをしっかり返せているか確認してみてください。おそらく以前のままでしたら、MyPageViewでpasswordはrerurnしていないと思います。
        # 以前から、stateを追加されたことが原因です。stateのみForeignKeyとなっていますので、JSONシリアライズできないとエラーが出ていました。基本的にForeignKeyやManyToManyFieldが含まれている場合は以前までの書き方ではうまく返せません。
        # そこで、今回のコードでserializerを用いてデシリアライズ（Model内のobjectを復元）してresponseで返すようにしています。
        return Response(data,status=status.HTTP_200_OK)

