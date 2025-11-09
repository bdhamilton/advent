import os
from datetime import datetime, date
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Advent calendar configuration
# Start date for the advent calendar (format: YYYY-MM-DD)
START_DATE = datetime.strptime(
    os.getenv('ADVENT_START_DATE', '2024-12-01'),
    '%Y-%m-%d'
).date()

# Ordered list of activities - same activity shown to all users on each day
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

def get_todays_activity():
    """
    Get today's activity based on the ordered list and start date.
    All users see the same activity on the same day.
    """
    today = date.today()

    # Calculate days since start date
    days_elapsed = (today - START_DATE).days

    # Get activity index (cycles through the list if we go past the end)
    activity_index = days_elapsed % len(ACTIVITIES)

    return ACTIVITIES[activity_index]

@app.route('/')
def index():
    """Main page - display today's advent activity"""
    activity = get_todays_activity()

    today = date.today()
    day_of_month = today.day

    return render_template('index.html',
                         activity=activity,
                         day=day_of_month,
                         month=today.strftime('%B'))

if __name__ == '__main__':
    # Only enable debug mode if explicitly set in environment
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
