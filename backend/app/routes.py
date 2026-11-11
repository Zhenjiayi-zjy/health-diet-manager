from flask import Blueprint, request
from app import db
from app.models import User, Food, DietRecord
from app.utils import APIResponse, APIException

main_bp = Blueprint('main', __name__)

# 健康检查接口
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

    return APIResponse.success(data=user.to_dict(), message="登录成功")

# 添加饮食记录
@main_bp.route('/api/diet/add', methods=['POST'])
def add_diet():
    data = request.get_json()
    record = DietRecord(
        user_id=data.get('user_id'),
        food_id=data.get('food_id'),
        amount=data.get('amount'),
        meal_type=data.get('meal_type', '午餐')
    )
    db.session.add(record)
    db.session.commit()
    return APIResponse.success(data=record.to_dict(), message="记录添加成功")

# 获取某用户的饮食记录列表
@main_bp.route('/api/diet/list/<int:user_id>', methods=['GET'])
def diet_list(user_id):
    records = DietRecord.query.filter_by(user_id=user_id).order_by(DietRecord.eaten_at.desc()).all()
    return APIResponse.success(data=[r.to_dict() for r in records])

# 搜索食物
@main_bp.route('/api/food/search', methods=['GET'])
def search_food():
    keyword = request.args.get('keyword', '')
    foods = Food.query.filter(Food.name.like(f'%{keyword}%')).all()
    return APIResponse.success(data=[f.to_dict() for f in foods])

# 每日热量统计
@main_bp.route('/api/diet/daily-summary', methods=['GET'])
def daily_summary(user_id):
    from datetime import datetime
    today = datetime.now().date()
    records = DietRecord.query.filter(
        DietRecord.user_id == user_id,
        db.func.date(DietRecord.eaten_at) == today
    ).all()

    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0

    for r in records:
        food = r.food
        if food:
            # 按比例计算：实际重量 / 100 * 每100g含量
            ratio = r.amount / 100
            total_calories += food.calories * ratio
            total_protein += food.protein * ratio
            total_fat += food.fat * ratio
            total_carbs += food.carbs * ratio

    return APIResponse.success(data={
        "date": str(today),
        "total_calories": round(total_calories, 1),
        "total_protein": round(total_protein, 1),
        "total_fat": round(total_fat, 1),
        "total_carbs": round(total_carbs, 1),
        "record_count": len(records)
    })
