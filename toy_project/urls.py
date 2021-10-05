from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # 以下がルートとなるurl
    path('', include('accounts.urls')),
    path('', include('find_retro_toys.urls')), #ここ追記
    # djoserとはDjango REST Framework上での基本的なユーザー認証や登録などの認証周りをサポートしてくれるライブラリです。
    # 参考文献
    # https://qiita.com/KueharX/items/eef29ae0c5c238cbf61c
    path('auth/', include('djoser.urls.jwt')),
    #追加
    #api/authアプリケーションのURLconf読み込み
    path('api/v1/auth/', include('djoser.urls.jwt')),
]

# 参考記事
# https://intellectual-curiosity.tokyo/2019/03/08/django%E3%81%A7%E7%94%BB%E5%83%8F%E3%82%92%E8%A1%A8%E7%A4%BA%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/
# imageなどのファイルは静的ファイルに属するので，静的ファイルを示すstaticファイルをプロジェクト内で読み込めるよう設定をする必要があります．
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)