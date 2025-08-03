"""finance_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from finance_app import views
from finance_app import auth_views

# 创建API路由器
api_router = DefaultRouter()
api_router.register(r"records", views.FinanceRecordViewSet, basename="financerecord")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/finance/", include(api_router.urls)),  # API路由
    # 认证相关API
    path("api/auth/login/", auth_views.login_api, name="login_api"),
    path("api/auth/register/", auth_views.register_api, name="register_api"),
    path("api/auth/logout/", auth_views.logout_api, name="logout_api"),
    path("api/auth/status/", auth_views.user_status_api, name="user_status_api"),
    # 认证页面
    path("auth/login/", auth_views.login_page, name="login_page"),
    path("auth/register/", auth_views.register_page, name="register_page"),
    path("", include("finance_app.urls")),  # 前端页面路由
]

# 在开发环境中提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
