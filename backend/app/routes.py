from flask import Blueprint, request
from app import db
from app.models import User, Food, DietRecord
from app.utils import APIResponse, APIException, generate_token, login_required

main_bp = Blueprint('main', __name__)

# 健康检查
@main_bp.route('/api/health', methods=['GET'])
def health():
    return APIResponse.success(message="后端服务正常运行中")

# 用户注册
@main_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise APIException("用户名和密码不能为空")

    if User.query.filter_by(username=username).first():
        raise APIException("用户名已存在")

    user = User(username=username, email=data.get('email'))
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return APIResponse.success(data=user.to_dict(), message="注册成功")

# 用户登录
@main_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        raise APIException("用户名或密码错误")

    token = generate_token(user.id)
    return APIResponse.success(
        data={"token": token, "user": user.to_dict()},
        message="登录成功"
    )

# 获取当前用户信息
@main_bp.route('/api/user/info', methods=['GET'])
def user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException("用户不存在", 404)
    return APIResponse.success(data=user.to_dict())

# 添加饮食记录
@main_bp.route('/api/diet/add', methods=['POST'])
def add_diet(user_id):
    data = request.get_json()
    record = DietRecord(
        user_id=user_id,
        food_id=data.get('food_id'),
        amount=data.get('amount'),
        meal_type=data.get('meal_type', '午餐')
    )
    db.session.add(record)
    db.session.commit()
    return APIResponse.success(data=record.to_dict(), message="记录添加成功")

# 获取某用户的饮食记录列表
@main_bp.route('/api/diet/list', methods=['GET'])
def diet_list(user_id):
    records = DietRecord.query.filter_by(user_id=user_id).order_by(DietRecord.eaten_at.desc()).all()
    return APIResponse.success(data=[r.to_dict() for r in records])
