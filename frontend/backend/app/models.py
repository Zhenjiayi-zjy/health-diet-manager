from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    diet_records = db.relationship('DietRecord', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)   # 每100g热量(千卡)
    protein = db.Column(db.Float, default=0)          # 蛋白质(g/100g)
    fat = db.Column(db.Float, default=0)              # 脂肪(g/100g)
    carbs = db.Column(db.Float, default=0)            # 碳水(g/100g)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "calories": self.calories,
            "protein": self.protein,
            "fat": self.fat,
            "carbs": self.carbs
        }


class DietRecord(db.Model):
    __tablename__ = 'diet_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)       # 食用重量(g)
    eaten_at = db.Column(db.DateTime, default=datetime.now)
    meal_type = db.Column(db.String(20), default='午餐')  # 早餐/午餐/晚餐/加餐

    food = db.relationship('Food')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "food": self.food.to_dict() if self.food else None,
            "amount": self.amount,
            "eaten_at": self.eaten_at.strftime("%Y-%m-%d %H:%M:%S"),
            "meal_type": self.meal_type
        }
