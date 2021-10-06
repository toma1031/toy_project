# DjangoRESTFrameworkでは、forms.pyのかわりにSerializers.pyでデータの入出力形式を扱います。
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import Post

# PostReadSerializerは読み込み専用
class PostReadSerializer(serializers.ModelSerializer):
    # StringRelatedField は読み込み専用
    # StringRelatedField は、 __str__ メソッドを使用して関係のターゲットを表すために使用できます。とあるように、ForeignKeyとしているモデルの_str_メソッドで定義しているfieldを返してくれます。今回だと、ConditionTagモデルでcondition_tagを_str_メソッドで定義しているため、StringRelatedFieldでcondition_tagを返してくれます。
    condition = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    # API画面で表示するモデルのフィールドをfieldsに記載
    class Meta:
        model = Post
        fields = ('id', 'title', 'maker', 'condition', 'price', 'description', 'user', 'shipping_price', 'photo', 'photo2', 'photo3', 'photo4', 'photo5',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'maker', 'condition', 'price', 'description', 'user', 'shipping_price', 'photo', 'photo2', 'photo3', 'photo4', 'photo5',)
