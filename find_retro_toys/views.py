from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import authentication, permissions, generics, routers
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from .serializers import PostSerializer
from .models import Post, ConditionTag
from accounts.models import User
from rest_framework.decorators import action
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import base64


# ListAPIViewを使うときは「モデルに紐付かない＋レコード一覧の取得」をしたいときです。その他のGeneric Viewもその種類によって用途が分かれておりますが、ModelViewSetで事足りる場合はGeneric Viewはほぼ使いません。
# 例えば、Postモデルに対して何か特別な処理を記述したいときは、大概はPostのModelViewSetに加筆するだけで処理が記述できます。
# ex )
# Postオブジェクト作成時に何らかのカスタマイズしたい
# 　　⇨ def create() メソッドを追加
# Postオブジェクトにいいね機能を実装したい
# 　　⇨ @action(detail=True, permission_classes=[IsAuthenticated])
#                  def like(self, request, pk=None):
# 　　　のようなアクションメソッドを追加
# DRFは、Djangoのように専用Viewを作ってテンプレートに渡す、という考え方ではありません。ですのでListAPIViewではなく、ユーザーモデルのようにModelViewSetを作成することで基本的なCRUD処理は可能です。また、投稿一覧を未ログインでも閲覧可能にする場合は、PermissionはAllowAnyにする必要があります。
# https://qiita.com/AJIKING/items/29327b7f7c46e2245505
class PostViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.AllowAny,)
  queryset = Post.objects.all()
  serializer_class = PostSerializer

  # 参考資料
  # https://just-python.com/document/django/orm-query/values-values_list
  # Viewをカスタマイズする場合は，取得したPostオブジェクトから，そのconditonのIDに紐づくconditionモデルの名前・userのIDに基づくユーザー名を返す処理を記述します．
  def get_queryset(self):
    # Postモデルのオブジェクト一覧から，user・condition_tagのみプライマリーキーでないものを取得し，それらを返す　といった処理を記述する必要があります．
    # 現状のモデルの構造から，Postのオブジェクトを取得してもそのcondition_tagはプライマリーキーであるIDが表示されます．
    # Viewをカスタマイズする場合，そのcondition_tagのIDに対応する文字列？を取得し，返す必要があります．
    user = User.objects.values('username')
    condition_tag = ConditionTag.objects.values('condition_tag')
    return user, condition_tag

  # get_queryset()関数を用いる場合はクエリセットを返す必要があるので，シリアライザーを用いてデシリアライズできない場合にエラーが出ます．
  # 今回の場合，condition_tag及びuserフィールドがプライマリーキーでないのでPostSerializerでデシリアライズできないため，自分でViewをカスタマイズする必要がありそうです．(*オブジェクトから文字列に変換する事をシリアライズ。(出力) 文字列からオブジェクトに変換する事をデシリアライズ。(入力)厳密にはシリアライズとは「DjangoのQuerySetsやモデルインスタンスをレンダリングしやすい形式にフォーマットすること」，デシリアライズとは「JSONなどのデータをpythonが扱えるデータ形式に変換すること」を指します)
  # 例ですが，アクションハンドラを用いて以下のように記述することで手動で欲しいデータ（userのユーザー名や，condition_tagのタグ名）をJSON化して返すことができます．
  # この場合，アクションハンドラを用いているので，loalhost:8000/posts/get_data/
  # にアクセスすると下記の結果を得られます．
  # ModelViewSetやModelSerializerをデフォルトで使うと全て自動でうまく返してくれるのですが、カスタマイズを加えると自動で処理してくれている部分についても自分で記述する必要がある
  # https://try2explore.com/questions/jp/10415173
  # https://www.fixes.pub/program/178801.html
  # serializers.py 内の request.build_absolute_uri で公開用URLを取得できるようです。
  @action(detail=False)
  # detailで指定するのは，「一覧 or 詳細」で今回はdetail=Falseと指定しているので一覧Viewという意味です．
  # 今回の目的はPostの一覧を取得することですので，一覧Viewですが，例えば一つ一つのPostの情報を取得したい場合は，詳細viewを指定します．
  # 詳細viewの場合はpkの記述が必要となり，アクションメソッドが多くなってくると分かりにくくなるので僕は一覧viewの場合（pk=None）も記述していますが，pkについては記述しなくても動きます！
  def get_data(self, request):
      obj = Post.objects.all()
      data = []
      for i in obj:
          # （例）以下のようにprint()することで，コンソールでphotoFieldのタイプが確認できます
          # print(type(i.photo))
          # serializer に指定するためのオブジェクトを1件ずつ取得している
          obj = Post.objects.get(id=i.id)
          # serializerの第一引数にオブジェクトを指定し，シリアライズ①
          # シリアライズで読み出されたデータは，data属性に入っている
          serialize_data = PostSerializer(obj, context={"request": request}).data
          # photoのみ，serializerを用いてシリアライズしたdataを指定する
          photo = serialize_data['photo']
          photo2 = serialize_data['photo2']
          photo3 = serialize_data['photo3']
          photo4 = serialize_data['photo4']
          photo5 = serialize_data['photo5']
          data.append({'title':i.title,'maker':i.maker,'condition':i.condition.condition_tag,'price':i.price,'description':i.description,'user':i.user.username,'shipping_price':i.shipping_price, 'photo':photo, 'photo2':photo2, 'photo3':photo3, 'photo4':photo4, 'photo5':photo5})
      # HTTP通信にはstatusが指定でき，そのエラーコードでReact側でエラー表示を場合分けなどできます．HTTP_200_OKは成功という意味のstatusですので記述しなくでも問題はありません．
      # が，レスポンスにHTTPstatusを付加することを覚えるとエラー処理の際に役に立ちます．
      # statusコードは以下のページが参考になります．
      # https://www.django-rest-framework.org/api-guide/status-codes/
      return Response(data, status=status.HTTP_200_OK)