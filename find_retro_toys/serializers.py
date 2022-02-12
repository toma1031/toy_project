# DjangoRESTFrameworkでは、forms.pyのかわりにSerializers.pyでデータの入出力形式を扱います。
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import Post, MessageRoom, Message

# シリアライズとは、データをフロント（API）に返す際にJSON形式に変換すること
# デシリアライズとは、JSON形式のデータをpythonが扱えるデータ形式に変換すること　です。
# サーバーへ送信という概念は厳密には異なります。そもそもDjangoはサーバーサイド言語でありサーバーへ送信という概念は誤っています。
# ですので、上記に記述したとおりJSON形式に変換するのがシリアライズ・JSON形式からpythonが扱えるデータ形式に変換するのがデシリアライズ、です。
# 基本的には、フロントエンド（API）からリクエストされたデータを保存・更新する場合は [デシリアライズ]、DBにあるデータをフロントエンド（API）に返したい場合は [シリアライズ] を行います。

class PostSerializer(serializers.ModelSerializer):
    #user、conditionに関しては、DRFから取得しているデータは文字列となっています。編集を行う（select要素に対象のアイテムを初期値としてセットする）場合、IDと文字列両方取得する必要があると考えられます。
    username = serializers.SerializerMethodField()
    condition_name = serializers.SerializerMethodField()

    def get_username(self, obj):
        # 下記はPostモデルのuserフィールドに紐づいてあるusernameフィールドを返すという意味
        return obj.user.username

    def get_condition_name(self, obj):
        # 下記はPostモデルのcondiotionフィールドに紐づいてあるcondition_tagフィールドを返すという意味
        return obj.condition.condition_tag

    # API画面で表示するモデルのフィールドをfieldsに記載
    class Meta:
        model = Post
        fields = ('id', 'title', 'maker', 'condition', 'price', 'description',
                  'user', 'username', 'condition_name', 'shipping_price',
                  'photo', 'photo2', 'photo3', 'photo4', 'photo5')
        read_only_fields = ('id', 'user', 'username', 'condition_name')


class MessageRoomSerializer(serializers.ModelSerializer):

    #SerializerMethodField()で定義している新たなフィールドです。このカスタマイズがない元々のコードでは、MessageRoomモデルには'post', 'inquiry_user', 'update_time'のフィールドのみが返されています。が、今回はRoomに紐づくMessageも返したいので新たにmessagesという出力専用フィールドを用意しています。
    messages = serializers.SerializerMethodField()
    # こちら以前にも登場しましたが、MethodFieldで定義したフィールド（今回はmessages）の中身をget_<field名>で指定します。
    # つまり、
    # field名 = serializers.SerializerMethodField()
    # def get_field名(self,obj):
    # return field名の中身
    # と記述することでModelにないデータもserializerで同時に出力できるようになります。おそらく以前Postの部分でもMethodFieldを用いていたと思うので再度見直してみてください。
    def get_messages(self,obj):
        data = []
        # オブジェクト.モデル名（小文字）_set.all()で紐づくモデルを取得可能です。今回ですと、obj.message_set.all()とすることでMessageRoomに紐づいているMessageを取得可能です。
        for i in range(len(obj.message_set.all())):
            data.append(obj.message_set.all()[i])
        # 本来は、obj.message_set.all()で得られたMessageオブジェクトを‘messages’フィールドとして返したいのですが、
        # QueryDictはシリアライズされていないためエラーが出ます。
        # そこで一度dataという配列にリストとして保存したのち、MessageSerializerを用いてシリアライズしています。
        data = MessageSerializer(data,many=True).data
        return data
    class Meta:
        model = MessageRoom
        fields = ('id', 'post', 'inquiry_user', 'update_time', 'messages')


class MessageSerializer(serializers.ModelSerializer):
    message_user = serializers.SerializerMethodField()
    # 下記のようにformatの部分を好みに変更することで時間の表記が変更可能．
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    def get_message_user(self, obj):
        return obj.message_user.username

    # def get_create_time(self, obj):
    #     return obj.create_time
    class Meta:
        model = Message
        fields = ('message', 'message_room', 'message_user', 'create_time')