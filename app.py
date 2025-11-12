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
    "Have a snowball fight (with real or paper snowballs).",
    "Buy a new ornament.",
    "Have dinner under the Christmas tree.",
    "Send someone on a candy cane hunt.",
    "<a href='https://www.target.com/p/christmas-tree-house-gingerbread-house-kit-28-5oz-favorite-day-8482/-/A-85929069#lnk=sametab' target='_blank'>Decorate a gingerbread house.</a>",
    "<a href='https://www.target.com/p/christmas-tree-house-gingerbread-house-kit-28-5oz-favorite-day-8482/-/A-85929069#lnk=sametab' target='_blank'>Christmas music dance party!</a>",
    "Spend all day in Christmas PJs.",
    "<a href='https://www.uspsoperationsanta.com/getinvolved' target='_blank'>Write and send a letter to Santa.</a>",
    "<a href='https://www.southernliving.com/food/drinks/spike-store-bought-eggnog' target='_blank'>Drink (spiked?) eggnog.</a>",
    "Eat dinner by candlelight.",
    "<a href='https://designimprovised.com//2016/12/diy-christmas-present-wreath.html' target='_blank'>Do a holiday-themed craft.</a> (You'll need <a href='https://www.michaels.com/product/18-wire-wreath-frame-by-ashland-10174335?michaelsStore=1577&inv=20' target='_blank'>this</a> and <a href='https://www.amazon.com/Liliful-Christmas-Ornaments-Miniature-Decorations/dp/B0CCHSG7ZC/' target='_blank'>these</a>.)",
    "<a href='https://www.amazon.com/gp/video/detail/B09PQDYN2R/ref=atv_sr_fle_c_sr62ef6f_1_1_1?sr=1-1&pageTypeIdSource=ASIN&pageTypeId=B09PQKZJYZ&qid=1762890220649' target='_blank'>Have a Christmas movie night.</a>",
    "Go caroling.",
    "<a href='https://smittenkitchen.com/2019/12/unfussy-sugar-cookies/' target='_blank'>Bake and decorate sugar cookies.</a>",
    "Deliver holiday treats to your neighbors.",
    "<a href='https://www.amazon.com/Mudpuppy-Merry-Catmas-Illustrations-Christmas/dp/0735386315/' target='_blank'>Complete a holiday-themed puzzle.</a>",
    "Wear a Santa hat to run errands.",
    "Donate to a local nonprofit.",
    "Attend a holiday-themed event.",
    "Take a drive to look at Christmas lights.",
    "Get a picture with Santa.",
    "<a href='https://www.marthastewart.com/266694/decorating-with-paper-snowflakes' target='_blank'>Make paper snowflakes.</a>",
    "Drink hot cocoa—bonus points if you doctor it with whipped cream, marshmallows, and sprinkles.",
    "Read The Night Before Christmas."
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
    today = date.today()
    completed = get_completed_activities()

    # Check if we're before the start date
    if today < START_DATE:
        return render_template('index.html',
                             before_start=True,
                             start_date=START_DATE,
                             activities_list=[])

    # Check if we're after all activities
    end_date = START_DATE + timedelta(days=len(ACTIVITIES) - 1)
    after_end = today > end_date

    # Build list of activities up to today (or all if after end)
    activities_list = []
    for i, act in enumerate(ACTIVITIES):
        activity_date = START_DATE + timedelta(days=i)

        # Skip future activities unless we're past the end
        if not after_end and activity_date > today:
            break

        is_today = activity_date == today and not after_end
        activities_list.append({
            'text': act,
            'date': activity_date,
            'completed': act in completed,
            'is_today': is_today
        })

    # Get current activity for display
    activity = get_todays_activity() if not after_end else None

    return render_template('index.html',
                         activity=activity,
                         day=today.day,
                         month=today.strftime('%B'),
                         completed=completed,
                         activities_list=activities_list,
                         before_start=False,
                         after_end=after_end)

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
    app.run(debug=debug_mode, host='0.0.0.0', port=5123)
