# DjangoRESTFrameworkでは、forms.pyのかわりにSerializers.pyでデータの入出力形式を扱います。
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer #追加
from .models import User, State


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

# API画面で表示するモデルのフィールドをfieldsに記載
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)
# def create()は、models.pyに記述してあるCustomUserManager内のcreate_userメソッドを呼び出しています。この部分を追加していなかったことが今回の一連のエラーの原因でした。
# ModelViewSetには、create()やupdate()メソッドが元々実装されているのですが、User関連のserializerだけパスワードのハッシュ化の関係でこのようにオーバーライドする必要があるそうです！
    def create(self,validated_data):
            user = User.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password']
            )
            return user

    def update(self, instance, validated_data):
        # もしパスワードがきちんと入力されていたら
        if 'password' in validated_data:
            # instanceというのは、このupdate()メソッドに入ったユーザーオブジェクトのことです。例えば、ユーザーAさんがプロフィールアップデートの処理をリクエストした際には、ユーザーAのUserModelオブジェクトが入ります！
            # update()メソッド内におけるvalidated_dataというのは、「更新リクエストを送ってきたユーザーの更新するフィールドのデータ」です。先ほどもパスワードのハッシュ化のためpasswordのみ特別な記述が必要と書いたのですが、それと同じであるユーザーが更新リクエストを送ってきた中にパスワードがあれば、このifの中に入り更新されるということです。
            instance.set_password(validated_data['password'])
        else:
            # こちらは更新リクエストにパスワードが入っていない場合の処理でして、その場合元々ModelSerializerに実装されているupdate()メソッドを用いて更新されます。superというのは、オーバーライドをするという意味でして、modelserializerに元々備えられているupdateメソッドを呼びますよという意味です。
            # パスワードが含まれている場合は、標準搭載のupdateメソッドを使わず、
            # 含まれていない場合は標準搭載のupdateメソッドを使う
            # という処理の流れになります。
            instance = super().update(instance, validated_data)
        instance.save()
        return instance

class StateSerializer(serializers.ModelSerializer):
    state = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = State
        # StateSerializerのfieldsの値が一つの場合リスト形式にする必要があるので、” , “を入れないとエラーが出ると思います。
        fields = ('state',)

    def create(self, validated_data):
        return State.objects.create_user(request_data=validated_data)


#トークンを発行するためのクラス
# トークンとはHTTPリクエストした時に発生する、暗号のようなもの
# このトークンをReactに送るというよりはDRF側ではReactに送信するといった処理は全くせずに、Tokenを発行するだけです。
# Token発行用のURLに、認証情報を持ってReactからやってきたユーザーが置かれているToken取りに来るようなイメージです。
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        # ユーザーのトークン（ユーザー情報）を取得
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 取得したらそのユーザー情報（トークン）を返す
        return token