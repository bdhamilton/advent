import os
from datetime import datetime, date
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/advent'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Advent calendar activities
ACTIVITIES = [
    "Drink hot cocoa with marshmallows",
    "Sing a Christmas carol",
    "Bake Christmas cookies",
    "Watch a holiday movie",
    "Make paper snowflakes",
    "Read a Christmas story",
    "Write a letter to Santa",
    "Decorate the Christmas tree",
    "Make homemade ornaments",
    "Light a festive candle",
    "Go caroling in the neighborhood",
    "Make a gingerbread house",
    "String popcorn garland",
    "Donate to a local charity",
    "Make holiday cards",
    "Have a snowball fight",
    "Build a snowman",
    "Go ice skating",
    "Visit a Christmas market",
    "Wrap presents with festive paper",
    "Look at Christmas lights",
    "Roast chestnuts",
    "Make a advent wreath",
    "Listen to Christmas music",
    "Have a cozy movie marathon"
]

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    activities = db.relationship('UserActivity', backref='user', lazy=True)

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity = db.Column(db.String(500), nullable=False)
    activity_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def get_or_create_user():
    """Get or create user based on session ID"""
    if 'user_id' not in session:
        session['user_id'] = os.urandom(16).hex()
    
    user = User.query.filter_by(session_id=session['user_id']).first()
    if not user:
        user = User(session_id=session['user_id'])
        db.session.add(user)
        db.session.commit()
    
    return user

def get_todays_activity(user):
    """Get or generate today's activity for the user"""
    today = date.today()
    
    # Check if user already has an activity for today
    existing_activity = UserActivity.query.filter_by(
        user_id=user.id,
        activity_date=today
    ).first()
    
    if existing_activity:
        return existing_activity.activity
    
    # Get all activities user has already seen
    seen_activities = [ua.activity for ua in user.activities]
    
    # Get unseen activities
    available_activities = [a for a in ACTIVITIES if a not in seen_activities]
    
    # If all activities have been seen, reset and use all activities
    if not available_activities:
        available_activities = ACTIVITIES
    
    # Select a random activity
    new_activity = random.choice(available_activities)
    
    # Save the activity
    user_activity = UserActivity(
        user_id=user.id,
        activity=new_activity,
        activity_date=today
    )
    db.session.add(user_activity)
    db.session.commit()
    
    return new_activity

@app.route('/')
def index():
    """Main page - display today's advent activity"""
    user = get_or_create_user()
    activity = get_todays_activity(user)
    
    today = date.today()
    day_of_month = today.day
    
    return render_template('index.html', 
                         activity=activity, 
                         day=day_of_month,
                         month=today.strftime('%B'))

@app.route('/new-activity', methods=['POST'])
def new_activity():
    """Get a new random activity for today (HTMX endpoint)"""
    user = get_or_create_user()
    
    # Delete today's activity to get a new one
    today = date.today()
    UserActivity.query.filter_by(
        user_id=user.id,
        activity_date=today
    ).delete()
    db.session.commit()
    
    # Get a new activity
    activity = get_todays_activity(user)
    
    return f'<div class="activity" id="activity">{activity}</div>'

@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized successfully!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
