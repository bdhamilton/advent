# Advent Calendar 🎄

A simple Flask web application that displays ordered Advent calendar activity ideas. All users see the same activity on the same day, progressing through a predetermined sequence. Built with a minimal stack focusing on simplicity.

## Features

- 🎁 **Daily Activities**: Get a festive activity suggestion each day in a predetermined order
- 👥 **Consistent Experience**: All users see the same activity on the same day
- 🗓️ **Configurable Start Date**: Set your own start date for the activity sequence
- 🎨 **Beautiful UI**: Festive, responsive design that works on all devices
- 📱 **No JavaScript Required**: Works perfectly without JavaScript enabled
- 🚀 **No Database Required**: Stateless design for easy deployment

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML/CSS
- **Configuration**: Environment variables with python-dotenv

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/bdhamilton/advent.git
cd advent
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure the application**
```bash
# Create a .env file from the example
cp .env.example .env

# Edit .env to customize:
# - SECRET_KEY: Set a unique secret key for sessions
# - ADVENT_START_DATE: Set your advent calendar start date (default: 2024-12-01)
# - FLASK_DEBUG: Set to 'true' for development mode
```

## Running the Application

**For development** (with debug mode for auto-reload and detailed errors):
```bash
# Set FLASK_DEBUG=true in your .env file, then run:
python app.py
```

**For production** (debug mode disabled by default):
```bash
python app.py
```

**Open your browser**
Navigate to `http://localhost:5000`

## Usage

- Visit the homepage to see today's Advent activity
- Each day, a new activity from the ordered list is displayed
- All users see the same activity on the same day
- The sequence starts from your configured `ADVENT_START_DATE`
- Activities cycle through the list in order (25 activities total)

## Project Structure

```
advent/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   └── css/
│       └── style.css      # Application styles
└── README.md              # This file
```

## How It Works

1. **Stateless Design**: No database or user tracking required - completely stateless
2. **Date-Based Calculation**: Activity is determined by calculating days elapsed since `ADVENT_START_DATE`
3. **Ordered Sequence**: Activities are displayed in the order they appear in the `ACTIVITIES` list
4. **Automatic Cycling**: After 25 days, the sequence repeats from the beginning using modulo arithmetic
5. **Consistent Experience**: All users see the same activity on the same day

## Customization

### Modifying Activities

Edit the `ACTIVITIES` list in `app.py` to customize the activity sequence:

```python
ACTIVITIES = [
    "Your first activity",
    "Your second activity",
    # ... add as many as you want
]
```

### Changing the Start Date

Set the `ADVENT_START_DATE` in your `.env` file:
```
ADVENT_START_DATE=2024-12-01
```

The format is `YYYY-MM-DD`. The first activity will be shown on this date.

## Production Deployment

For production deployment:

1. Set a strong `SECRET_KEY` in your environment variables
2. Configure your `ADVENT_START_DATE` appropriately
3. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn app:app
```
4. Consider using a reverse proxy like Nginx
5. The application is stateless, so it scales horizontally without any shared state concerns

## License

MIT License - feel free to use this project for your own Advent calendar!
