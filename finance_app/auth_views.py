from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def login_page(request):
    """登录页面"""
    if request.user.is_authenticated:
        return redirect("index")
    return render(request, "auth/login.html")


def register_page(request):
    """注册页面"""
    if request.user.is_authenticated:
        return redirect("index")
    return render(request, "auth/register.html")


@csrf_exempt
@require_http_methods(["POST"])
def login_api(request):
    """登录API"""
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse(
                {"success": False, "message": "用户名和密码不能为空"}, status=400
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(
                {
                    "success": True,
                    "message": "登录成功",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": "用户名或密码错误"}, status=401
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "请求数据格式错误"}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"登录失败: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["POST"])
def register_api(request):
    """注册API"""
    try:
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # 验证输入
        if not all([username, email, password, confirm_password]):
            return JsonResponse(
                {"success": False, "message": "所有字段都是必填的"}, status=400
            )

        if password != confirm_password:
            return JsonResponse(
                {"success": False, "message": "两次输入的密码不一致"}, status=400
            )

        if len(password) < 6:
            return JsonResponse(
                {"success": False, "message": "密码长度至少为6位"}, status=400
            )

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"success": False, "message": "用户名已存在"}, status=400
            )

        # 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"success": False, "message": "邮箱已被注册"}, status=400
            )

        # 创建用户
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        # 自动登录
        login(request, user)

        return JsonResponse(
            {
                "success": True,
                "message": "注册成功",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "请求数据格式错误"}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"注册失败: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["POST"])
def logout_api(request):
    """登出API"""
    try:
        logout(request)
        return JsonResponse({"success": True, "message": "已成功登出"})
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"登出失败: {str(e)}"}, status=500
        )


def user_status_api(request):
    """获取用户状态API"""
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "authenticated": True,
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                },
            }
        )
    else:
        return JsonResponse({"authenticated": False})
