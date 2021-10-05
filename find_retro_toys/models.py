from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class ConditionTag(models.Model):
  condition_tag = models.CharField(verbose_name='ConditionTag', max_length=20, null=False, blank=False)
  # 以下を書くことによりcategoryをちゃんとオブジェクト名で表示できる
  def __str__(self):
    return self.condition_tag

class Post(models.Model):
  title = models.CharField(verbose_name='Title', max_length=40, null=False, blank=False)
  maker = models.CharField(verbose_name='Maker', max_length=40, null=False, blank=False)
  condition = models.ForeignKey(ConditionTag, verbose_name='Condition', on_delete=models.CASCADE)
  price = models.IntegerField(verbose_name='Price',null=False, blank=False)
  description = models.TextField(verbose_name='Description', max_length=300, null=False, blank=False)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='user')
  shipping_price = models.IntegerField(verbose_name='Shipping Price',null=False, blank=False)
  # 写真は５枚アップロードできるようにする
  photo = models.ImageField(upload_to='images/', verbose_name='Photo', null=False, blank=False)
  photo2 = models.ImageField(upload_to='images/', verbose_name='Photo2', null=True, blank=True)
  photo3 = models.ImageField(upload_to='images/', verbose_name='Photo3', null=True, blank=True)
  photo4 = models.ImageField(upload_to='images/', verbose_name='Photo4', null=True, blank=True)
  photo5 = models.ImageField(upload_to='images/', verbose_name='Photo5', null=True, blank=True)

# 以下を書くことによりcategoryをちゃんとオブジェクト名で表示できる
  def __str__(self):
    return self.condition

class MessageRoom(models.Model):
    post = models.ForeignKey(Post, verbose_name='MessageRoom Post', on_delete=models.CASCADE)
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
    message_room = models.ForeignKey(MessageRoom, verbose_name='Message', on_delete=models.CASCADE)
    message_user = models.ForeignKey(get_user_model(), verbose_name='message_user', on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
      return str(self.id)