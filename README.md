# Social Media Engagement Tracker API

This project is a Django RESTful API with Celery background tasks to monitor social media profiles, track follower counts, and send Telegram notifications for engagement milestones.

## Features
- Register/update social media profiles to monitor
- Set/retrieve alert settings for follower milestones
- Fetch latest follower count and engagement insights
- Basic authentication for API
- Background task (Celery) to periodically check follower counts (mocked)
- Telegram bot notifications for milestones
- **Top follower insights**: Track the top follower count increases or decreases in the last 24 hours
- **Mock profile data**: Simulates follower count changes for testing

## Setup

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Redis (for Celery):**
   ```bash
   redis-server
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser (optional, for admin):**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run Django server:**
   ```bash
   python manage.py runserver
   ```
6. **Start Celery worker:**
   ```bash
   celery -A hami worker --loglevel=info
   ```
7. **Start Celery Beat (for periodic tasks):**
   ```bash
   celery -A hami beat --loglevel=info
   ```

### Docker Compose (Recommended)

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```
   This will start:
   - Django (web API)
   - Celery worker
   - Celery Beat (periodic tasks)
   - Redis (broker)

2. **Access the API:**
   - Django: [http://localhost:8000](http://localhost:8000)
   - API root: [http://localhost:8000/api/](http://localhost:8000/api/)

## API Endpoints
- `/api/profiles/` : Register or update a profile
- `/api/alerts/` : Set or retrieve alert settings
- `/api/follower-counts/` : Fetch latest follower count and insights
- `/api/profiles/top-insights/` : **Get top follower increases and decreases in the last 24 hours**

## Telegram Bot
- Set your Telegram bot token in `api/tasks.py` (`YOUR_BOT_TOKEN`)

## Mock Data
- Follower counts are simulated for testing purposes using random increments/decrements.

## Notes
- Uses SQLite by default (see `settings.py`)
- All endpoints require basic authentication
- See `.gitignore` for recommended files to exclude from version control 