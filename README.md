# Advent Calendar 🎄

A simple Flask/HTMX web application that displays a random Advent calendar activity idea to users each day. Built with a lean stack focusing on simplicity.

## Features

- 🎁 **Daily Activities**: Get a random festive activity suggestion each day
- 🔄 **Dynamic Updates**: Use HTMX for seamless, interactive experiences without heavy JavaScript
- 💾 **User State**: PostgreSQL database tracks which activities each user has seen
- 🎨 **Beautiful UI**: Festive, responsive design that works on all devices

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTMX for dynamic interactions
- **Database**: PostgreSQL for user state persistence
- **ORM**: SQLAlchemy for database operations

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
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

4. **Set up PostgreSQL database**
```bash
# Create a PostgreSQL database
createdb advent

# Or using psql:
psql -U postgres
CREATE DATABASE advent;
\q
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

6. **Initialize the database**
```bash
flask init-db
```

## Running the Application

1. **Start the Flask development server**
```bash
python app.py
```

2. **Open your browser**
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
2. **Database Tracking**: User activities are stored in PostgreSQL with dates
3. **Activity Selection**: Each day, a random activity is selected from unseen activities
4. **HTMX Integration**: The "Get Another Idea" button uses HTMX to fetch new activities without page reload

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
