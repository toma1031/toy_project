from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth import get_user_model
from phone_field import PhoneField

# UserManagerはUserモデルの上に通常記載します！カスタムユーザーを作成する場合には必ず作成しないとうまくいかないみたいです。
class CustomUserManager(UserManager):
    # """ユーザーマネージャー"""
    use_in_migrations = True


    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        # emailのドメインを小文字に変換
        email = self.normalize_email(email)
        # UserProfileモデルを参照してuserを定義
        user = self.model(email=email, username=username)
        # userが入力したパスワードをハッシュ化
        user.set_password(password)
        # settings.pyでdefaultに設定されているDBに保存
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

# Create your models here.
class State(models.Model):
    state = models.CharField(verbose_name='State', max_length=20, unique=True)

    def __str__(self):
      return self.state
class User(AbstractUser):
    email = models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')
    state = models.ForeignKey(State,verbose_name='State', on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(verbose_name='City', max_length=20, blank=True, null=True)
    address = models.CharField(verbose_name='Address', max_length=50, blank=True, null=True)
    zipcode = models.CharField(verbose_name='Zip Code',max_length=5, blank=True, null=True)
    phone_number = PhoneField(blank=True)
    # CustomUserManagerを使う際は下記の記載が必ず必要。
    objects = CustomUserManager()