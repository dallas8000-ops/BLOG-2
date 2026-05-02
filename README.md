
# BLOG-2

A professional Django blog application with full CRUD functionality, REST API, JWT authentication, social login, real-time notifications, and advanced search/filtering.

## Features
- Create, Read, Update, and Delete (CRUD) for blog posts
- User authentication (login, logout, signup, social login with Google/GitHub)
- User profiles with avatars, bio, social links, and roles (admin, editor, author, reader)
- REST API for posts and users (Django REST Framework)
- JWT authentication for API access
- Real-time notifications (Django Channels, WebSockets)
- Full-text search and advanced filtering for posts (web & API)
- Responsive, modern Bootstrap-based UI
- Validation and error handling

## API Endpoints
- `/api/posts/` - List, create, update, delete posts (JWT required for write)
- `/api/users/` - List users
- `/api/token/` - Obtain JWT token
- `/api/token/refresh/` - Refresh JWT token

## Real-Time Notifications
- WebSocket endpoint: `ws/notifications/`
- Users receive notifications when new posts are created

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/dallas8000-ops/BLOG-2.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
6. Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Social Authentication Setup
- Go to Django admin > Social Applications to add Google/GitHub client IDs and secrets.
- Set the site domain to `localhost:8000` for local development.

## Project Structure
- `posts/` - Blog post app (models, views, templates, signals)
- `accounts/` - User authentication and profiles
- `api/` - REST API endpoints and serializers
- `notifications/` - Real-time notification consumers and utils
- `templates/` - HTML templates
- `static/` - CSS, images, JS

## Contribution Guidelines
1. Fork the repository and create your branch from `master`.
2. Write clear, concise commit messages.
3. Add tests for new features and ensure all tests pass.
4. Submit a pull request with a description of your changes.

## Author
- Dallas8000-ops

---
This project is for educational and portfolio purposes. Contributions welcome!
