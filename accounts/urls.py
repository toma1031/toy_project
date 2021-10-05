# from django.conf.urls import include, path
# from rest_framework import authentication, routers
# # from .views import AuthRegister, AuthInfoGetView, AuthInfoUpdateView, AuthInfoDeleteView
# from .views import AuthInfoViewSet
# from django.urls import include, path

# app_name = 'accounts'

# urlpatterns = [
#     url(r'^register/$', AuthRegister.as_view()),
#     url(r'^mypage/$', AuthInfoGetView.as_view()),
#     url(r'^auth_update/$', AuthInfoUpdateView.as_view()),
#     url(r'^delete/$', AuthInfoDeleteView.as_view()),
# ]


# router = DefaultRouter()
# # AuthInfoという名前のModelViewSetの場合、以下の記述のみでCRUD処理可能
# router.register(‘user’,views.AuthInfoViewSet)
# urlpatterns = [
#     path(‘’, include(router.urls)),
# ]


from django.urls import path, include
from django.conf.urls import url
from accounts import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from accounts.views import MyPageView, MyPagePasswordUpdateView

router = DefaultRouter()
# Viewでquerysetの記述があればbasenameの設定はいらない
router.register(r'users',views.UserViewSet)
# アクションメソッドがない場合は以下
# router.register('users',views.UserViewSet)
urlpatterns = [
    # 上でDefaultRouterに定義したurlが登録されAPIコンソールに表示される
    path('', include(router.urls)),
    # path('auth/', include('djoser.urls.jwt')),
    url(r'^mypage/$', MyPageView.as_view()),
    url(r'^mypage_password_update/$', MyPagePasswordUpdateView.as_view()),
]
