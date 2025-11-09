# Advent Calendar 🎄

A simple Flask/HTMX web application that displays a random Advent calendar activity idea to users each day. Built with a lean stack focusing on simplicity.

## Features

- 🎁 **Daily Activities**: Get a random festive activity suggestion each day
- 🔄 **Dynamic Updates**: Simple form-based interaction for getting new activities
- 💾 **User State**: Database tracks which activities each user has seen
- 🎨 **Beautiful UI**: Festive, responsive design that works on all devices
- 📱 **No JavaScript Required**: Works perfectly without JavaScript enabled

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML/CSS with simple form submissions
- **Database**: PostgreSQL (production) or SQLite (development/testing)
- **ORM**: SQLAlchemy for database operations

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ (optional - SQLite used by default for development)
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

4. **Set up the database**

For development, SQLite is used by default (no setup needed).

For production with PostgreSQL:
```bash
# Create a PostgreSQL database
createdb advent

# Or using psql:
psql -U postgres
CREATE DATABASE advent;
\q

# Set DATABASE_URL environment variable
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

5. **Initialize the database**
```bash
flask init-db
```

6. **Start the Flask development server**
```bash
python app.py
```

7. **Open your browser**
Navigate to `http://localhost:5000`

## Usage

- Visit the homepage to see today's Advent activity
- Click "✨ Get Another Idea" to get a different activity suggestion
- Each day you'll get a new random activity from the calendar
- The app remembers which activities you've seen to avoid repetition

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

1. **User Sessions**: Each visitor gets a unique session ID stored in a cookie
2. **Database Tracking**: User activities are stored in the database (SQLite by default, PostgreSQL in production) with dates
3. **Activity Selection**: Each day, a random activity is selected from unseen activities
4. **Form Submission**: The "Get Another Idea" button submits a form to fetch a new activity

## Database Schema

### Users Table
- `id`: Primary key
- `session_id`: Unique session identifier
- `created_at`: Timestamp of user creation

### User Activities Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `activity`: The activity text
- `activity_date`: Date the activity was assigned
- `created_at`: Timestamp of record creation

## Development

To modify the activities list, edit the `ACTIVITIES` array in `app.py`.

## Production Deployment

For production deployment:

1. Set a strong `SECRET_KEY` in your environment variables
2. Update `DATABASE_URL` with your production database credentials
3. Set `debug=False` in the Flask app configuration
4. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn app:app
```

## License

MIT License - feel free to use this project for your own Advent calendar!
