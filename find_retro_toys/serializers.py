# DjangoRESTFrameworkでは、forms.pyのかわりにSerializers.pyでデータの入出力形式を扱います。
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import Post

# PostReadSerializerは読み込み専用
# class PostReadSerializer(serializers.ModelSerializer):
#     # StringRelatedField は読み込み専用
#     # StringRelatedField は、 __str__ メソッドを使用して関係のターゲットを表すために使用できます。とあるように、ForeignKeyとしているモデルの_str_メソッドで定義しているfieldを返してくれます。今回だと、ConditionTagモデルでcondition_tagを_str_メソッドで定義しているため、StringRelatedFieldでcondition_tagを返してくれます。
#     # condition = serializers.StringRelatedField()

#     username = serializers.SerializerMethodField()
#     def get_username(self,obj):
#         return obj.user.username
#     # conditionに関しては、DRFから取得しているデータは文字列となっています。編集を行う（select要素に対象のアイテムを初期値としてセットする）場合、これもuserと同様にIDと文字列両方取得する必要があると考えられます。
#     condition_name = serializers.SerializerMethodField()
#     def get_condition_name(self,obj):
#         # 下記はPostモデルのcondiotionフィールドに紐づいてあるcondition_tagフィールドを返すという意味
#         return obj.condition.condition_tag
#     # API画面で表示するモデルのフィールドをfieldsに記載
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'maker', 'condition', 'condition_name', 'price', 'description', 'user', 'username', 'shipping_price', 'photo', 'photo2', 'photo3', 'photo4', 'photo5',)


# class PostSerializer(serializers.ModelSerializer):

# # 現在userフィールドは、serializer.is_valid()を満たした場合にserializer.save(user=self.request.user)で保存するようにしています。こちらはserializers.pyを修正することでバリデーションエラーが無くなると思います。
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'maker', 'condition', 'price', 'description', 'user', 'shipping_price', 'photo', 'photo2', 'photo3', 'photo4', 'photo5',)
#         read_only_fields = ('id','user')






class PostSerializer(serializers.ModelSerializer):
    #user、conditionに関しては、DRFから取得しているデータは文字列となっています。編集を行う（select要素に対象のアイテムを初期値としてセットする）場合、IDと文字列両方取得する必要があると考えられます。
    username = serializers.SerializerMethodField()
    condition_name = serializers.SerializerMethodField()
    def get_username(self,obj):
        # 下記はPostモデルのuserフィールドに紐づいてあるusernameフィールドを返すという意味
        return obj.user.username
    def get_condition_name(self,obj):
        # 下記はPostモデルのcondiotionフィールドに紐づいてあるcondition_tagフィールドを返すという意味
        return obj.condition.condition_tag
    # API画面で表示するモデルのフィールドをfieldsに記載
    class Meta:
        model = Post
        fields = ('id', 'title', 'maker', 'condition', 'price', 'description', 'user', 'username', 'condition_name', 'shipping_price', 'photo', 'photo2', 'photo3', 'photo4', 'photo5')
        read_only_fields = ('id','user','username','condition_name')