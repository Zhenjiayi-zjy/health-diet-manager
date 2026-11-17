from flask import Blueprint, request
from app import db
from app.models import User, Food, DietRecord
from app.utils import APIResponse, APIException, generate_token, login_required
from datetime import datetime, timedelta


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

# 搜索食物
# 搜索食物
@main_bp.route('/api/food/search', methods=['GET'])
def search_food():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        return APIResponse.success(data=[])
    foods = Food.query.filter(Food.name.like(f'%{keyword}%')).all()
    return APIResponse.success(data=[f.to_dict() for f in foods])


# 每日热量统计
@main_bp.route('/api/diet/daily-summary', methods=['GET'])
@login_required
def daily_summary(user_id):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_start = today_start + timedelta(days=1)
    
    records = DietRecord.query.filter(
        DietRecord.user_id == user_id,
        DietRecord.eaten_at >= today_start,
        DietRecord.eaten_at < tomorrow_start
    ).all()

    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    valid_count = 0

    for r in records:
        food = r.food
        if food:
            ratio = r.amount / 100
            total_calories += food.calories * ratio
            total_protein += food.protein * ratio
            total_fat += food.fat * ratio
            total_carbs += food.carbs * ratio
            valid_count += 1

    return APIResponse.success(data={
        "date": today_start.strftime("%Y-%m-%d"),
        "total_calories": round(total_calories, 1),
        "total_protein": round(total_protein, 1),
        "total_fat": round(total_fat, 1),
        "total_carbs": round(total_carbs, 1),
        "record_count": valid_count
    })

# ==================== 扩展功能接口 ====================

# 删除饮食记录
@main_bp.route('/api/diet/<int:record_id>', methods=['DELETE'])
@login_required
def delete_diet(user_id, record_id):
    record = DietRecord.query.filter_by(id=record_id, user_id=user_id).first()
    if not record:
        raise APIException('记录不存在', 404)
    db.session.delete(record)
    db.session.commit()
    return APIResponse.success(message='删除成功')


# 近7天统计
@main_bp.route('/api/diet/weekly-summary', methods=['GET'])
@login_required
def weekly_summary(user_id):
    from datetime import timedelta
    today = datetime.now().date()
    start_date = today - timedelta(days=6)
    
    records = DietRecord.query.filter(
        DietRecord.user_id == user_id,
        DietRecord.eaten_at >= start_date,
        DietRecord.eaten_at < today + timedelta(days=1)
    ).all()
    
    # 按天分组
    daily_data = {}
    for i in range(7):
        day = start_date + timedelta(days=i)
        daily_data[str(day)] = 0
    
    for r in records:
        food = r.food
        if food:
            day_str = r.eaten_at.strftime('%Y-%m-%d')
            daily_data[day_str] = daily_data.get(day_str, 0) + food.calories * (r.amount / 100)
    
    result = [{"date": k, "calories": round(v, 1)} for k, v in sorted(daily_data.items())]
    return APIResponse.success(data=result)


# 设置每日目标
@main_bp.route('/api/user/goal', methods=['PUT'])
@login_required
def update_goal(user_id):
    data = request.get_json()
    goal = data.get('daily_goal')
    if not goal or goal <= 0:
        raise APIException('请输入有效的热量目标', 400)
    
    user = User.query.get(user_id)
    user.daily_goal = goal
    db.session.commit()
    return APIResponse.success(message='目标设置成功')


# 获取每日目标
@main_bp.route('/api/user/goal', methods=['GET'])
@login_required
def get_goal(user_id):
    user = User.query.get(user_id)
    return APIResponse.success(data={"daily_goal": user.daily_goal})
