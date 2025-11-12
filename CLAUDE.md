# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Flask-based Advent calendar web application that displays daily activity suggestions in a predetermined sequence. All users see the same activity on the same day, calculated from a configurable start date. Features a Price is Right-style wheel interface with HTMX for seamless interactivity.

## Key Architecture Concepts

### Date-Based Activity System
- **Stateless design**: No database required; all state calculated from `START_DATE` and `ACTIVITIES` list
- Activity determination: `(today - START_DATE).days % len(ACTIVITIES)` gives consistent activity index for all users
- Activities cycle through the predefined list indefinitely using modulo arithmetic
- Session storage tracks individual completion status only (not shared across users)

### HTMX Integration
- Two distinct toggle endpoints with different return patterns:
  - Today's activity (no `index` param): returns `_today_activity_form.html` partial
  - List activities (with `index` param): returns `_activity_item.html` partial
- HTMX swaps are targeted to specific DOM elements via `hx-target` and `outerHTML` swap
- JavaScript wheel listens to `htmx:afterSwap` events to refresh items after updates

### Wheel Display System
- `ActivityWheel` class manages 3D-style rotating list with perspective scaling
- Center item always at index `currentIndex`, others positioned relative with transform/scale/opacity
- "Today's" activity auto-centered on page load via `findTodayIndex()`
- Supports multiple input methods: buttons, mouse wheel, keyboard arrows, clicking items

## Common Commands

### Development
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with debug mode (set FLASK_DEBUG=true in .env first)
python app.py

# Run tests
python test_htmx.py
```

### Configuration
- Edit `.env` to set:
  - `SECRET_KEY`: Flask session secret
  - `ADVENT_START_DATE`: First day of activity sequence (YYYY-MM-DD format)
  - `FLASK_DEBUG`: Enable debug mode for development

### Production Deployment
```bash
pip install gunicorn
gunicorn app:app
```

## Important Implementation Details

- Server runs on port 5123 by default (see `app.py:153`)
- Activities list in `app.py:21-47` defines the sequence and can be modified
- Template partials (`_activity_item.html`, `_today_activity_form.html`) must maintain matching structure to main `index.html` for HTMX swaps
- Checkbox `onchange` events trigger form submission via `dispatchEvent` for progressive enhancement
- Session-based completion tracking means cleared sessions reset user's completion state
