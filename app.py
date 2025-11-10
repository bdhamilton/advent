import os
from datetime import datetime, date, timedelta
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
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

def get_activity_for_date(target_date):
    """
    Get the activity for a specific date.
    """
    days_elapsed = (target_date - START_DATE).days
    activity_index = days_elapsed % len(ACTIVITIES)
    return ACTIVITIES[activity_index]

def get_completed_activities():
    """
    Get the set of completed activities from session.
    Returns a set of activity strings.
    """
    if 'completed_activities' not in session:
        session['completed_activities'] = []
    return set(session['completed_activities'])

def toggle_activity_completion(activity):
    """
    Toggle the completion status of an activity.
    """
    completed = get_completed_activities()
    if activity in completed:
        completed.remove(activity)
    else:
        completed.add(activity)
    session['completed_activities'] = list(completed)
    session.modified = True

@app.route('/')
def index():
    """Main page - display today's advent activity"""
    activity = get_todays_activity()
    completed = get_completed_activities()

    today = date.today()
    day_of_month = today.day

    # Build list of all activities with their dates and completion status
    activities_list = []
    for i, act in enumerate(ACTIVITIES):
        activity_date = START_DATE + timedelta(days=i)
        activities_list.append({
            'text': act,
            'date': activity_date,
            'completed': act in completed,
            'is_today': act == activity
        })

    return render_template('index.html',
                         activity=activity,
                         day=day_of_month,
                         month=today.strftime('%B'),
                         completed=completed,
                         activities_list=activities_list)

@app.route('/toggle-activity', methods=['POST'])
def toggle_activity():
    """Toggle the completion status of an activity"""
    activity = request.form.get('activity')
    index = request.form.get('index')

    if activity and activity in ACTIVITIES:
        toggle_activity_completion(activity)

    # Get updated completion status
    completed = get_completed_activities()
    today_activity = get_todays_activity()

    # If this is from the activities list (has index), return the activity item partial
    if index is not None:
        index = int(index)
        activity_date = START_DATE + timedelta(days=index)
        item = {
            'text': ACTIVITIES[index],
            'date': activity_date,
            'completed': ACTIVITIES[index] in completed,
            'is_today': ACTIVITIES[index] == today_activity
        }
        return render_template('_activity_item.html', item=item, index=index)

    # Otherwise, return the today's activity form partial
    return render_template('_today_activity_form.html',
                         activity=today_activity,
                         completed=completed)

if __name__ == '__main__':
    # Only enable debug mode if explicitly set in environment
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
