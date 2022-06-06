from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import authentication, permissions, generics, routers
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from .serializers import PostSerializer, MessageSerializer, MessageRoomSerializer, LikeSerializer
from .models import Post, ConditionTag, Message, MessageRoom, Like
from accounts.models import User
from rest_framework.decorators import action
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import base64
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
import django_filters.rest_framework


# class PostViewSet(viewsets.ModelViewSet):

#     permission_classes = (permissions.AllowAny,)
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def create(self, request, pk=None):
#         print("Here is create()")
#         # photo2 ~ photo5 は指定しなくても良いフィールドだと思いますが、
#         # 例えばphoto のみを指定してリクエストを送った場合、上記の部分でphoto2 に request.data['photo2'] を指定してしまっている、つまりImageFieldに空のデータを入力しているからエラーが出てしまっています。
#         # 「request.data に photo2 が含まれるなら、photo2 フィールドにそれを指定」
#         # のように場合分けをする処理を追加する必要があると思います。
#         # if request.data['photo2'] and request.data['photo3'] and request.data['photo4'] and request.data['photo5']:
#         #     data={'title':request.data['title'], 'maker': request.data['maker'], 'condition': request.data['condition'], 'price':
#         # コード簡略化のため下記のように辞書に追加していく形でも良いかと思います。
#         # 辞書オブジェクト[キー] = 値
#         # とすることで辞書を上書きできます。
#         data = {'title': request.data['title'], 'maker': request.data['maker'], 'condition': request.data['condition'], 'price': request.data['price'],
#                 'description': request.data['description'], 'shipping_price': request.data['shipping_price'], 'photo': request.data['photo']}
#         if request.data['photo2']:
#             data['photo2'] = request.data['photo2']
#         elif request.data['photo3']:
#             data['photo3'] = request.data['photo3']
#         elif request.data['photo4']:
#             data['photo4'] = request.data['photo4']
#         elif request.data['photo5']:
#             data['photo5'] = request.data['photo5']

#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             # userField のみここでリクエストユーザーに設定する
#             # User項目がDRFのAPIコンソールで表示されないのは、下記のコードのせい（user を手動で設定しているからです。）
#             # axios リクエストには user を含めず、DRF 側でPostオブジェクトの保存時に、user = リクエストユーザー として保存する
#             # 「Postを投稿（保存）する際に、userフィールドはリクエストしてきたユーザーをDRF側で識別して保存する」と設定しているためAPIコンソールでuserフィールドを選択させる必要がないということになります！\        serializer.save(user=self.request.user)
#             print("Post created")
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # DRF側のdef create()内で保存できなかった場合にはBad Request を返す
#         # React側で、DRFからBad Request（status 400）を受け取ったら、エラーを表示させる（Postがうまく作成できていないという情報）
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         print(serializer.errors)
#         print(serializer.is_valid())
#         print(serializer)
#         print(request.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     # def create(self, request):
#     #       print(request.data)

#     #       return Response("test", status=status.HTTP_200_OK)

#     # 参考資料
#     # https://just-python.com/document/django/orm-query/values-values_list
#     # Viewをカスタマイズする場合は，取得したPostオブジェクトから，そのconditonのIDに紐づくconditionモデルの名前・userのIDに基づくユーザー名を返す処理を記述します．
#     # def get_queryset(self):
#     #   # Postモデルのオブジェクト一覧から，user・condition_tagのみプライマリーキーでないものを取得し，それらを返す　といった処理を記述する必要があります．
#     #   # 現状のモデルの構造から，Postのオブジェクトを取得してもそのcondition_tagはプライマリーキーであるIDが表示されます．
#     #   # Viewをカスタマイズする場合，そのcondition_tagのIDに対応する文字列？を取得し，返す必要があります．
#     #   user = User.objects.values('username')
#     #   condition_tag = ConditionTag.objects.values('condition_tag')
#     #   return user, condition_tag

#     # 下記はPost一覧用
#     # get_queryset()関数を用いる場合はクエリセットを返す必要があるので，シリアライザーを用いてデシリアライズできない場合にエラーが出ます．
#     # 今回の場合，condition_tag及びuserフィールドがプライマリーキーでないのでPostSerializerでデシリアライズできないため，自分でViewをカスタマイズする必要がありそうです．(*オブジェクトから文字列に変換する事をシリアライズ。(出力) 文字列からオブジェクトに変換する事をデシリアライズ。(入力)厳密にはシリアライズとは「DjangoのQuerySetsやモデルインスタンスをレンダリングしやすい形式にフォーマットすること」，デシリアライズとは「JSONなどのデータをpythonが扱えるデータ形式に変換すること」を指します)
#     # 例ですが，アクションハンドラを用いて以下のように記述することで手動で欲しいデータ（userのユーザー名や，condition_tagのタグ名）をJSON化して返すことができます．
#     # この場合，アクションハンドラを用いているので，loalhost:8000/posts/get_data/
#     # にアクセスすると下記の結果を得られます．
#     # ModelViewSetやModelSerializerをデフォルトで使うと全て自動でうまく返してくれるのですが、カスタマイズを加えると自動で処理してくれている部分についても自分で記述する必要がある
#     # https://try2explore.com/questions/jp/10415173
#     # https://www.fixes.pub/program/178801.html
#     # serializers.py 内の request.build_absolute_uri で公開用URLを取得できるようです。

#     @action(detail=False)
#     # detailで指定するのは，「一覧 or 詳細」で今回はdetail=Falseと指定しているので一覧Viewという意味です．
#     # 今回の目的はPostの一覧を取得することですので，一覧Viewですが，例えば一つ一つのPostの情報を取得したい場合は，詳細viewを指定します．
#     # 詳細viewの場合はpkの記述が必要となり，アクションメソッドが多くなってくると分かりにくくなるので僕は一覧viewの場合（pk=None）も記述していますが，pkについては記述しなくても動きます！
#     def get_data(self, request):

#       # Postオブジェクトを取得
#         queryset = Post.objects.all()
#       # serializer変数にPostReadSerializerを読み込むように設定
#         serializer = PostReadSerializer
#         # querysetをserializer（ここではPostReadSerializer）を用いてシリアライズし、そのデータを変数dataに格納
#         data = serializer(queryset, many=True, context={
#                           "request": request}).data
#         # 取得したデータを返す
#         return Response(data, status=status.HTTP_200_OK)

#     # 下記はPostDetail用
#     @action(detail=True)
#     #  get_data()はdetail=Falseとなっていますよね？これは、一覧Viewという意味です。これのdetail=Trueのアクションメソッドを、追加しなければなりません。
#     # get_data()はdetail=Falseとなっていますよね？これは、一覧Viewという意味です。これのdetail=Trueのアクションメソッドを、追加しなければなりません。
#     # @action(detail=True)
#     #     def get_data_detail(self, request, pk):
#     # 上の様なものを新たに作ることで、
#     # /posts/pk/get_data_detail
#     # で参照可能になると思います。
#     def get_data_detail(self, request, pk):
#         # Postオブジェクトを取得
#         # queryset = Post.objects.all()
#         # @action()を用いて定義している　get_data() や　get_data_detail() はModelViewSetとは独立に働きます。
#         # get_data()では、
#         # queryset = Post.objects.all()
#         # としているため一覧でPostのデータが取得されます。
#         # それに対して get_data_detail()では、
#         # queryset = Post.objects.get(id=self.kwargs['pk'])
#         # と指定し、idがURLパラメータと一致する一つのPostのデータのみを取得します。
#         queryset = Post.objects.get(id=self.kwargs['pk'])
#       # serializer変数にPostReadSerializerを読み込むように設定
#         serializer = PostReadSerializer
#         # querysetをserializer（ここではPostReadSerializer）を用いてシリアライズし、そのデータを変数dataに格納
#         data = serializer(queryset, context={
#                           "request": request}).data
#         # 取得したデータを返す
#         return Response(data, status=status.HTTP_200_OK)


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
    permission_classes = (permissions.AllowAny, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # 検索機能
    # https://www.utakata.work/entry/python/django/rest-framework/filter#REST-framework-%E3%81%AE%E8%A9%B3%E7%B4%B0%E3%81%AA%E4%BB%95%E6%A7%98
    # https://www.django-rest-framework.org/api-guide/filtering/
    # DjangoFilterBackendとSearchFilterを使えば良いと思います。
    # DjangoFilterBackendは、filterset_fieldsで指定したフィールドに対してのみ、完全一致でのフィルタが可能になります。
    # ex) 投稿者がAさんのPost の検索
    # SearchFilter は、search_fieldsで指定したフィールドに対してのみ、キーワード検索を可能にします。
    # ex) タイトルに“Switch”が含まれるPostの検索
    # ちなみに他にOrderingFilterでは、オーダリング（ソート）が可能になります。
    # DjangoFilterBackend を使うには、django-filter をインストールし、 django_filters を Django の INSTELLED_APPS に追加する必要がありますので、この辺は調べると例がたくさん出てくると思います。
    # Reactとの繋げ方はシンプルです。
    # DRFでフィルターの設定ができると、写真のようにAPIコンソールでフィルタリングできるようになります。
    # このURLがエンドポイントとなるので、React側でそれに合わせてAxiosリクエストを送れば良いということです。
    # 例として、PostModelViewSetでDjangoFilterBackendを使うとします。「ユーザーtestさんが投稿したPostを検索」します。
    # すると、URLは
    # /posts/?owner=test
    # のように変化します。このURLにReact側でGetリクエストを送ると、「ユーザーtestさんが投稿したPost」のみが返ってくるという流れです。
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'maker']

    # http://note.crohaco.net/2018/django-rest-framework-serializer/
    # 上記の記事で非常に詳しく説明されていますが、
    # serializerでは、create と update メソッドが 状況に応じて呼び出されます。
    # この状況というのが引数の数です。
    # create
    # def create():
    # では
    # serializer = self.serializer_class(data=data)
    # dataというのは、新規作成したいオブジェクトのデータです。
    # update
    # def update():
    # では
    # serializer = self.serializer_class(obj, data=data, partial=True)
    # objとは、更新対象のオブジェクト
    # dataとは、更新したいデータ
    # partial=True を指定すると、一部更新可能になります。
    # 仮にpartial=Trueが指定されていないと
    # serializer = self.serializer_class(obj, data=data)
    # dataには対象オブジェクトの全てのFieldを指定する必要があります。
    # 分かりやすい例を考えるとあるUserモデルに、name・email・passwordフィールドがあるとします。
    # Userを新規作成したい場合
    # serializer = self.serializer_class(data={'name':'tanaka','email':'tanaka@gmail.com','password':'pass'})
    # if serializer.is_valid():
    # serializer.save()
    # としてcreate()を呼び出します。
    # 上で作成したUser（tanakaさん）を更新（一部更新としてemailのみ変更）したい場合
    # obj = User.obujects.get(name="tanaka")
    # serializer = self.serializer_class(obj, data={'email':'new@gmail.com'}, partial=True)
    # objで更新対象のオブジェクト（ここではtanakaさん）を指定し、そのUserの一部のフィールドを更新しています。
    # このように、引数の数でcreateとupdateを状況に応じて呼び出しています。

    def create(self, request, pk=None):
        data = {
            'title': request.data['title'],
            'maker': request.data['maker'],
            'condition': request.data['condition'],
            'price': request.data['price'],
            'description': request.data['description'],
            'shipping_price': request.data['shipping_price'],
            'photo': request.data['photo']
        }
        if request.data['photo2']:
            data['photo2'] = request.data['photo2']
        elif request.data['photo3']:
            data['photo3'] = request.data['photo3']
        elif request.data['photo4']:
            data['photo4'] = request.data['photo4']
        elif request.data['photo5']:
            data['photo5'] = request.data['photo5']
        # print(data)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # userField のみここでリクエストユーザーに設定する
            # axios リクエストには user を含めず、DRF 側でPostオブジェクトの保存時に、user = リクエストユーザー として保存する
            # userField のみここでリクエストユーザーに設定する
            # User項目がDRFのAPIコンソールで表示されないのは、下記のコードのせい（user を手動で設定しているからです。）
            # axios リクエストには user を含めず、DRF 側でPostオブジェクトの保存時に、user = リクエストユーザー として保存する
            # 「Postを投稿（保存）する際に、userフィールドはリクエストしてきたユーザーをDRF側で識別して保存する」と設定しているためAPIコンソールでuserフィールドを選択させる必要がないということになります！
            serializer.save(user=self.request.user)
            # print("Post created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, partial=True):
        # update()に入っているか & リクエストデータ確認用
        print(request.data)
        obj = Post.objects.get(id=pk)

        data = {
            'title': request.data['title'],
            'maker': request.data['maker'],
            'condition': request.data['condition'],
            'price': request.data['price'],
            'description': request.data['description'],
            'shipping_price': request.data['shipping_price'],
        }
        # request.dataとは、Reactからリクエストしているデータです。
        # request.data['photo']は、React側のformdata
        # つまり、
        # if request.data['１、ここのphotoはなにのPhotoを指しているのか？React？DRF?'] != 'null':
        # この質問の答えは、Reactからリクエストしたデータの‘photo’です。
        # つまり下記のIF文はReactからPhotoがNullじゃなかったら（つまりPhotoが送られてきたら）
        if request.data['photo'] != 'null':
            #  DRFでアップデートするために用意しているdata変数に、ReactのPhotoデータ（Updateしたもの）を追加
            data['photo'] = request.data['photo']
        if request.data['photo2'] != 'null':
            data['photo2'] = request.data['photo2']
        if request.data['photo3'] != 'null':
            data['photo3'] = request.data['photo3']
        if request.data['photo4'] != 'null':
            data['photo4'] = request.data['photo4']
        if request.data['photo5'] != 'null':
            data['photo5'] = request.data['photo5']

        # objとは、更新対象のオブジェクト
        # dataとは、更新したいデータ
        # partial=True を指定すると、一部更新可能になります。
        serializer = self.serializer_class(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    ## フォロー判断用
    # 関数名がURLに追加されるのは、
    # （考え方としては、URLに働き・処理が追加されるイメージです）
    # アクションメソッドを用いた関数を定義した時のみです。
    # なのでアクセスするエンドポイントURLは
    # http://127.0.0.1:8000/posts/PostのID/open_messageroom
    # になる
    # MessageRoomViewSetを加筆されていますが、MessageRoomを開く際には、
    # /posts/ID/open_messageroom/ のエンドポイントにアクセスしていますよね？
    # つまり、これはPostViewSet内に記述しているアクションメソッドopen_messageroom()であり、MessageRoomViewSetは使っていないという意味です！！
    @action(detail=True, permission_classes=[IsAuthenticated])
    def open_messageroom(self, request, pk):
        #  新規Roomの作成にはget_or_createを用いると良いと思います。
        # get_or_create()の使い方は以下の通りです。
        # オブジェクトが存在しない場合は、DBにオブジェクトを登録して登録した値を返し、オブジェクトが存在する場合は、DBにオブジェクトを登録せずに値を返す
        # ですので、オブジェクトが存在するか存在しないかで返される値が変わります。
        # objには取得または作成されたオブジェクト・creaetdには新しいオブジェクトが作成されたかどうかを指定するブール値が返ります。
        # objには、指定するMessageRoomオブジェクトがあった場合getしたMessageRoomオブジェクトが返され、指定するMessageRoomオブジェクトがなかった場合は新たに登録されたMessageRoomオブジェクトが返されます。
        # createdは、新たなオブジェクトが登録された場合（指定するMessageRoomオブジェクトがなかった場合）True、登録されなかった場合（指定するMessageRoomオブジェクトがあった場合）にはFalseが返されます。
        # このように、get_or_createを用いると、対象とするユーザーとPostに紐づくMessageRoomがある場合とまだ存在しない場合とを簡単に場合分けて処理することが可能です。
        # https://docs.djangoproject.com/en/4.0/ref/models/querysets/
        obj, created = MessageRoom.objects.get_or_create(inquiry_user=request.user, post=self.get_object())
        # 下記でMessageRoomオブジェクトデータをフロントエンドへ送るためJSON化の準備をしている
        serializer = MessageRoomSerializer(obj)
        # 投稿主、質問者がそれぞれ適切なメッセージルームのURLを開くには
        # Postのオーナー情報（今回post.userとして取得しようとしている値）まで含めるようにDRFからのレスポンスを修正する
        # DRF側で オーナー＝質問者 となる場合にエラーを返し、そのエラーステータスを元にReact側でエラーハンドリングする
        # これらの解決策がありますが、下の方のDRFを修正する方が賢明です。
        # 理由としては、DRFを今のまま修正せずReact側で場合分け処理をする場合
        # レスポンスを元にリダイレクト or MessageRoomの表示を分岐しているので、一度MessageRoomは作られてしまいます。
        # オーナー=質問者のMessageRoomが余分にDBに追加されることになりますので
        # その余分なMessageRoomが作られる前にDRF側で対処する方が良いということです。
        # DRFのopen_messageroom()内を修正してみてください。
        # 具体的には、
        # if オーナー == 質問者:
        # return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        # というような処理を追加すれば良いと思います。
        # そうすると、React側で
        # if (レスポンスstatus === 406){
        # history.push("リダイレクト先URL");
        # }
        # 複雑な処理を記述する必要がなくなり、statusコードのみで簡単にリダイレクト処理を記述可能です。
        if obj.post.user == obj.inquiry_user:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        # MessageRoomが既存の場合
        else:
            if not created:
                # MessageRoomとそのRoom内のMessageを返す
                # 下記のコードで上の下準備されたデータをJSON化している（何々.dataでJSON化できる、これをシリアライズという）
                print("not created")
                # HTTP_200_OKは「リクエストは成功しレスポンスとともに要求に応じたリソースが返される。」という意味です。
                # 参照https://www.django-rest-framework.org/api-guide/status-codes/
                return Response(serializer.data, status=status.HTTP_200_OK)
            # MessageRoomがまだ存在しない場合
            else:
            # 新規Roomを作成
                # objは必ずシリアライズしてResponseしなければなりません。
                print("created")
                # HTTP_201_CREATEDは「リクエストは完了し新たにリソースが作成された。」という意味です。
                # 参照https://www.django-rest-framework.org/api-guide/status-codes/
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    # お気に入り
    @action(detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        # リクエストユーザーと対象ポストに紐付くLikeオブジェクトを作成
        obj, created = Like.objects.get_or_create(user=request.user, post=self.get_object())
        # 下記でLikeオブジェクトデータをフロントエンドへ送るためJSON化の準備をしている
        serializer = LikeSerializer(obj)
        print(request.user)
        if created:
            print("created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Likeが既存の場合
        else:
            print("not created")
            # お気に入りを取り除く
            obj.delete()
            # HTTP_200_OKは「リクエストは成功しレスポンスとともに要求に応じたリソースが返される。」という意味です。
            # 参照https://www.django-rest-framework.org/api-guide/status-codes/
            return Response("Delete Like Object", status=status.HTTP_200_OK)
        
 
                
class MessageRoomViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = MessageRoom.objects.all()
    serializer_class = MessageRoomSerializer

    # Get関数でメッセージルームにアクセスできるユーザーを制限
    def get(self, request, **kwargs):
        # message_room_obj変数にMessageroomオブジェクトのIDを入れ込む
        message_room_obj = get_object_or_404(MessageRoom, pk=self.kwargs['pk'])
        # 投稿したユーザー(message_room_obj.post.userとログイン中のユーザー(self.request.user)が一致する、もしくは
        # メッセージルームを作ったユーザー（message_room_obj.inquiry_user）とログイン中のユーザー（self.request.user）が一致すれば、メッセージルームへ移動させる
        if message_room_obj.post.user == self.request.user or message_room_obj.post.inquiry_user == self.request.user:
            # super(). = MessageRoomViewクラスに設定しているListViewのこと
            # **kwargs　＝　ここではその前のコードでmessage_room_obj=get_object_or_404(MessageRoom, pk=self.kwargs['pk'])としているから、message_roomのIDのことをさす。つまりreturn super().get(request, **kwargs)を詳しくいうと
            # ListViewで設定したmessage_roomのIDを探して（GET）、それを返す
            return super().get(request, **kwargs)
        else:
            # メッセージルームのメンバーでない場合はIndexへ飛ばす
            return redirect('/')

    # 送信済みのメッセージを表示するために必要
    def get_context_data(self, **kwargs):
        # contextという変数にMessageRoomViewSet（ここではsuperがMessageRoomViewSetを表している）のContextデータ（context_object_name = 'message_room'）をGetして辞書型として代入
        # この時点で変数contextにはmessage_roomが辞書型で入っている。
        context = super().get_context_data(**kwargs)
        # message_listをContextとして定義。contextは辞書型のデータなので、データを追加することもできる。例えば、context['message_list'] = 'message_room'とすれば、keyがmessage_list、valueがMessage.objects.all()というデータを追加することができる。
        # つまり、下記のように書くことによりcontextをどういうものにするか定義していることになる
        # Message.objects.filter(message_room_id=self.kwargs['pk'])はMessageモデルのmessage_roomフィールドが今アクセスしてるMessageRoomのidと一致するものだけ持ってくるという意味。self.kwargs[‘pk’]はそのオブジェクトのIDという意味がある
        context['message_list'] = Message.objects.filter(message_room_id=self.kwargs['pk'])
        # 最後にContext（Message.objects.all()）を返す
        return context

    @action(detail=False, permission_classes=[IsAuthenticated])
    # detail=Falseの一覧Viewの時は、pk=Noneと指定しないとエラーが出ます。
    def my_messagerooms(self, request, pk=None):
        # ユーザーが投稿したPost
        # "user_posts"というのは、Postモデルにあるuserフィールドのrelated_name
        # つまりrequest.user.user_posts.all()はリクエストを送っているユーザーでpostに紐づくユーザーを全て取得という意味
        # それを変数user_postsに格納している
        user_posts = request.user.user_posts.all()
        # 質問者（inquiry_user）もしくはポストの投稿者(post.user)がログイン中ユーザー(self.request.user)となるオブジェクト
        # filterの文法について、まとめている記事はネット上にたくさんありますので是非調べてみてください。
        # filter()内の書き方としては、上記のようにuser_postと、オブジェクトだけ記述することはできません。user_postsにはPostオブジェクトが入っていますので、filter内にそれだけ記述しても、MessageRoomオブジェクトの何がuser_postと一致するものを選べば良いのか？理解できません。
        # ですので、MessageRoomオブジェクトの「postフィールドがuser_postに当てはまるものを選ぶ」などと具体的フィールドとともにフィルター処理を記述する必要があります。
        # フィールド名__in=とすることで、複数条件をINしてフィルターをかけることができます。この辺のfilterの文法については、調べてください。つまり、user_postsにはログイン中ユーザーが投稿したPostが複数入っているので、それらを複数条件としてフィルターをかけているということです。
        # 文法としては(モデルのフィールド=オブジェクト)
        obj= MessageRoom.objects.filter(Q(inquiry_user=request.user)|Q(post__in=user_posts))
        data = self.serializer_class(obj, many=True).data
        # MessageRoomがない場合のエラーハンドリング（400を返す部分）が一番下に記載されていますが、その上でも正常時のreturnが記載されていたので、エラーであっても正常時のreturnが適用されるようになっていました。以下のように、エラーハンドリングの際のif文の場所を変更しなければなりません。
        # メッセージルームがない場合
        if not obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data,status=status.HTTP_200_OK)


        # 上記まとめ

        # request.userはログイン中のユーザーという意味、
        # user_postsはPostモデルにあるuserフィールドのrelated_nameなのでPostを指しているのではなく
        # Postに紐づいているユーザー（投稿者）を指しているのではと思ったからです。
        # つまり
        # request.user.user_posts.all()
        # はログインしているユーザーでPostに紐づいているユーザー（投稿者）という意味で
        # ログイン中ユーザーの投稿Postというのは違うような気がしたのですが
        # 上記で自分は何を勘違いしていますでしょうか？
        # （つまりuser_posts変数にはPost投稿者でかつログインしているユーザーが格納されるという認識でいます。）
        # 逆参照の方法についての理解が必要です。今回の実装は、1⇨多の逆参照です。
        # まず、request.userはログイン中ユーザーを指すという解釈は正しいです。
        # user_postsはPostモデルにあるuserフィールドのrelated_nameです。ここまではOKです。
        # ここからが重要です。
        # request.user.user_posts.all()
        # 上記は、下の記述と同義です。
        # request.user.post_set.all()
        # これは、
        # インスタンス.モデル名（小文字）_set.all()の記述形式であり、逆参照の記法です。
        # つまり、「ログイン中ユーザーに紐づいている全てのPost」という意味です。
        # 上記の記述から、related_nameを利用した記述に変更したのが、
        # request.user.user_posts.all()
        # です。今回のrelated_nameは“user_posts”としているので、post_set → user_posts（モデル名（小文字）_set　→ related_name名）と書くことができるようになり、直感的に分かりやすくなります。
        # Userモデルに紐づいているPostが複数フィールドあるとき（likePost、stockPostなど）related_nameを付けないとエラーが出ます。今回は、Userモデルに紐づいているPostは1つだけだと思いますが、related_nameを用いて上記のように逆参照しているということです。

        # 上記はPostモデルの
        # userフィールドの記載ですが
        # userフィールドとは本来ユーザーを表現するものであって
        # Postを表現しているのではないと思っているのですが
        # 日本語訳がなぜ
        # 「ログイン中ユーザーに紐づいている全てのPost」
        # になるのかが分からないでおります。。
        # Postモデルのuserフィールドは、Userモデルに紐づいているForeignKeyです。
        # tomato様が混乱している原因は、今回逆参照を行っているのに、参照を行っていると誤認しているためだと考えられます。ですので、参照と逆参照についての理解が必要かと思います。
        # まずモデルを整理しましょう。簡単に、以下のようなモデルがあると考えてください。
        # class User(models.Model):
        #     name = models.CharField(max_length=100)

        # class Post(models.Model):
        #     title = models.CharField(verbose_name='Title', max_length=40, null=False, blank=False)
        #     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='user_posts')
        # 参照の場合　[ インスタンス.フィールド名 ]
        # post = Post.objects.get(title="post1")
        # post.user
        # とすることで、タイトルが “post1"というPostオブジェクトのuserを取得することが可能です。
        # 逆参照の場合　[ インスタンス.クラス名_set もしくは related_name ]
        # user = User.objects.get(name="hiroko")
        # user.post_set.all()
        # とすることで、nameが“hiroko”というUserオブジェクトと紐づいているPostを取得することが可能です。別に言い換えれば、hirokoさんの投稿したPostを取得するということです。
        # そして、昨日申し上げたようにpost_setという記述は、related_nameを用いるとuser_postsに書き換えることが可能です。
        # つまり、
        # user = User.objects.get(name="hiroko")
        # user.user_posts.all()
        # と書き換えることができ、これもhirokoさんの投稿したPostを取得するという処理です。
        # ですので、僕が送ったコードのこの部分で
        # user_posts = request.user.user_posts.all()
        # user_postsという変数に、「ログイン中ユーザーに紐づいている全てのPost」が入っているということです。
        # ここまでは大丈夫でしょうか？
        # その後に続くコードで
        # 質問者（inquiry_user）もしくはポストの投稿者(post.use)がログイン中ユーザー(self.request.user)となるオブジェクト
        # obj= MessageRoom.objects.filter(Q(inquiry_user=request.user)|Q(post__in=user_posts))
        # とありますが、フィルターをかけようとしているのは
        # ユーザーに対してですよね？
        # つまり、user_postsは日本語訳は
        # 「ログイン中ユーザーに紐づいている全てのPostのユーザー」
        # という認識でいるのですが、こちらは正しいでしょうか？
        # 先程までの部分を理解していただけたら、user_postsという変数には、「ログイン中ユーザーに紐づいている全てのPostのユーザー」ではなく、「ログイン中ユーザーに紐づいている全てのPost」が格納されていることが分かります。次はフィルターに意味についてです。
        # フィルターの条件を一つずつ理解しましょう。
        # (inquiry_user=request.user)
        # なんですが
        # (Messageroomモデルにあるフィールドで質問者を表すinquiry_userフィールド=ログイン中のユーザー)
        # という認識はただしいでしょうか？
        # こちらの解釈は正しいです。
        # 正しいとするなら
        # (post__in=user_posts)
        # の意味がよく分からないのですが、なにを勘違いしておりますでしょうか？
        # （モデルのフィールド名を記載=実際に入れ込みたいデータ）
        # というようなイメージおります。
        # 先程までの説明で、user_postsという変数には、ログイン中ユーザーの投稿Postが入っていると言いました。
        # ですので、このコードの意味は、MessageRoomオブジェクトのpostフィールドがuser_posts（ログイン中ユーザーの投稿Post）のものを取得しています。
        # フィールド名__in=とすることで、複数条件をINしてフィルターをかけることができます。この辺のfilterの文法については、調べてください。つまり、user_postsにはログイン中ユーザーが投稿したPostが複数入っているので、それらを複数条件としてフィルターをかけているということです。
        # ここまでがfilter条件の理解です。
        # つまり、
        # 質問者（inquiry_user）もしくはポストの投稿者(post.use)がログイン中ユーザー(self.request.user)となるオブジェクト
        # obj= MessageRoom.objects.filter(Q(inquiry_user=request.user)|Q(post__in=user_posts))
        # 上記のコードは上記のコメント通りのフィルターをかけたMessageRoomオブジェクトをobj変数に格納していることになります。
        # とありますが、フィルターをかけようとしているのは
        # ユーザーに対してですよね？
        # となると、この部分は誤解があり、フィルターをかけようとしているのは、inquiry_userフィールドとpostフィールドですので、ユーザーに対してのみではありません。
        # なぜかというと、一番初めにtomato様が記述されていたように、
        # (post.user = request.user)
        # というようなフィールドをネストしたフィルターはかけられないからです。
        # 上記のコードはMessageRoomオブジェクトに紐づいているpostの投稿主＝ログイン中ユーザーかと思いますが、tomato様のモデル構成では、これができません。
        # 仮に、MessageRoomモデルに新たに“post_user”のようなフィールドを追加し、そこに紐づいているPostの投稿者を保存する構成ならば
        # (post_user = request.user)
        # と記述するだけで良いので、
        # obj= MessageRoom.objects.filter(Q(inquiry_user=request.user)|Q(post_user=request.user))
        # と書くことができ、これはユーザーに対してのみのフィルターで済みます。
        # ですが、今回はMessageRoomモデルにそのようなフィールドは用意されていません。
        # ですので、わざわざuser_postsという変数に「ログイン中ユーザーに紐づいている全てのPost」を取得したのちに
        # それをフィルターに用いているということです。
        # もしどうしてもこのような逆参照が難しい場合は、
        # 先に申し上げた通りMessageRoomモデルにpostの投稿主（MessageRoomに紐づいているPostを投稿したユーザー）を格納するフィールドを作成し、それをフィルター条件に用いると良いかと思います。



class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, pk=None):
            # serializerの引数が一つの時は、create()が呼び出されるということを以前確認しました。
            # そして、create()が呼び出される際の引数には作成したいオブジェクトの中身を指定します。
            # 今回も同様、新たなMessageを作成したいので、その引数としてdataというオブジェクトを用意しています。
            # そしてそのdataの中に、‘message’や‘message_room’などの必要なfieldと値を以下の部分で指定しています。
            data = {
                'message': request.data['message'],
                'message_room': request.data['message_room'],
                'create_time': timezone.now(),
                'message_user': self.request.user.id,
            }
            # save()メソッドはDRFでは使えません．全てserializerを通して保存する必要があります．
            # こちらは、上に述べたようにserializerの引数にdataを与え、create()を呼び出している部分です。
            serializer = self.serializer_class(data=data)
            # そして、
            # if serializer.is_valid():
            # の後にバリデーションが成功した場合、
            # serializer.save()
            # でMessageオブジェクトを新規作成しているという流れです。
            # この部分です。
            # http://note.crohaco.net/2018/django-rest-framework-serializer/
            if serializer.is_valid():
                serializer.save(message_user=self.request.user)
                print("Message was sent")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)



# class LinkViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.AllowAny, )
#     queryset = Message.objects.all()
#     serializer_class = LinkSerializer

# class LikeViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.AllowAny, )
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer