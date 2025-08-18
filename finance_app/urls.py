from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建API路由器
router = DefaultRouter()
router.register(r"records", views.FinanceRecordViewSet, basename="financerecord")

# 定义app命名空间
app_name = "finance_app"

urlpatterns = [
    # 前端页面路由
    path("", views.index, name="index"),
    path("history/", views.history, name="history"),
    # API路由（当通过api/finance/访问时使用）
    path("", include(router.urls)),
]
