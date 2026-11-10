from flask import jsonify, request
import jwt
from datetime import datetime, timedelta

# 密钥，实际项目放配置里，课程项目先写死
SECRET_KEY = "diet-health-secret-key-2026"

class APIException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

class APIResponse:
    @staticmethod
    def success(data=None, message="成功"):
        return jsonify({
            "code": 200,
            "message": message,
            "data": data
        })

    @staticmethod
    def error(message="失败", code=400):
        return jsonify({
            "code": code,
            "message": message,
            "data": None
        })

def generate_token(user_id):
    """生成token"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)  # 7天有效期
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def login_required(f):
    """登录验证装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return APIResponse.error("未登录，请先登录", 401)
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data["user_id"]
        except:
            return APIResponse.error("token失效，请重新登录", 401)
        return f(user_id, *args, **kwargs)
    return decorated
