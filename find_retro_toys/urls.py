from django.urls import path, include
from find_retro_toys import views
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'find_retro_toys'
router = DefaultRouter()
router.register(r'posts',views.PostViewSet)

urlpatterns = [
    # 上でDefaultRouterに定義したurlが登録されAPIコンソールに表示される
    path('', include(router.urls)),
]


