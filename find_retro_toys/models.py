from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class ConditionTag(models.Model):
  condition_tag = models.CharField(verbose_name='ConditionTag', max_length=20, null=False, blank=False)
  # 以下を書くことによりcategoryをちゃんとオブジェクト名で表示できる
  def __str__(self):
    return str(self.condition_tag)

class Post(models.Model):
  title = models.CharField(verbose_name='Title', max_length=40, null=False, blank=False)
  maker = models.CharField(verbose_name='Maker', max_length=40, null=False, blank=False)
  condition = models.ForeignKey(ConditionTag, verbose_name='Condition', on_delete=models.CASCADE)
  price = models.IntegerField(verbose_name='Price',null=False, blank=False)
  description = models.TextField(verbose_name='Description', max_length=300, null=False, blank=False)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='user')
  shipping_price = models.IntegerField(verbose_name='Shipping Price',null=False, blank=False)
  # 写真は５枚アップロードできるようにする
  # photo = models.ImageField(upload_to='images/photo_from_user')
  # とすることで、media/images/photo_from_user/　にファイルが保存され、urlも同様にできるかと思います。
  photo = models.ImageField(verbose_name='Photo', null=False, blank=False, upload_to='images/photo_from_user')
  photo2 = models.ImageField(verbose_name='Photo2', null=True, blank=True, upload_to='images/photo_from_user')
  photo3 = models.ImageField(verbose_name='Photo3', null=True, blank=True, upload_to='images/photo_from_user')
  photo4 = models.ImageField(verbose_name='Photo4', null=True, blank=True, upload_to='images/photo_from_user')
  photo5 = models.ImageField(verbose_name='Photo5', null=True, blank=True, upload_to='images/photo_from_user')

# 以下を書くことによりcategoryをちゃんとオブジェクト名で表示できる
  def __str__(self):
    return str(self.title)

class MessageRoom(models.Model):
    # related_nameの使い方
    # 逆参照するときはクラス名ではなくrelated_nameを使うことで逆参照が可能となります。
    # https://djangobrothers.com/blogs/related_name/
    post = models.ForeignKey(Post, verbose_name='MessageRoom Post', related_name='messageroom_post', on_delete=models.CASCADE)
    inquiry_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='inquiry_user')
    update_time = models.DateTimeField(auto_now=True)

    # my_messages.htmlで最新のMessageを表示するために下記を追記、
    def get_last_message(self):
      # selfはMessageRoomオブジェクトのこと
      first_message_obj = self.message_set.all().order_by('-create_time').first()
      if first_message_obj:
          return first_message_obj.message
      else:
          return 'No massage yet'

    def __str__(self):
      return str(self.id)
      
class Message(models.Model):
    message = models.CharField(max_length=100)
    message_room = models.ForeignKey(MessageRoom, verbose_name='Message_room_id', on_delete=models.CASCADE)
    message_user = models.ForeignKey(get_user_model(), verbose_name='message_user', on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
      return str(self.id)


