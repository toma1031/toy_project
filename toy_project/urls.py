"""toy_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    # 以下がルートとなるurl
    path('', include('accounts.urls')),
    # djoserとはDjango REST Framework上での基本的なユーザー認証や登録などの認証周りをサポートしてくれるライブラリです。
    # 参考文献
    # https://qiita.com/KueharX/items/eef29ae0c5c238cbf61c
    path('auth/', include('djoser.urls.jwt')),
    #追加
    #api/authアプリケーションのURLconf読み込み
    path('api/v1/auth/', include('djoser.urls.jwt'))
]
