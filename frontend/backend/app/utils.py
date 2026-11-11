from flask import jsonify

class APIException(Exception):
    """自定义业务异常"""
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

class APIResponse:
    """统一返回格式"""
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
