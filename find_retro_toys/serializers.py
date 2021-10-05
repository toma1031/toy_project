# DjangoRESTFrameworkでは、forms.pyのかわりにSerializers.pyでデータの入出力形式を扱います。
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # ModelViewSetやModelSerializerをデフォルトで使うと全て自動でうまく返してくれるのですが、カスタマイズを加えると自動で処理してくれている部分についても自分で記述する必要がある
    # https://try2explore.com/questions/jp/10415173
    # https://www.fixes.pub/program/178801.html
    # serializers.py 内の request.build_absolute_uri で公開用URLを取得できるようです。
    photo = serializers.SerializerMethodField('get_photo')
    def get_photo(self, post):
            request = self.context.get('request')
            photo = post.photo.url
            return request.build_absolute_uri(photo)
    # API画面で表示するモデルのフィールドをfieldsに記載
    class Meta:
        model = Post
        fields = ('id','title', 'maker', 'condition', 'price', 'description', 'user', 'shipping_price', 'photo', 'photo2', 'photo3', 'photo4', 'photo5',)
