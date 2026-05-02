
# BLOG-2

A production Django blog and portfolio site deployed on Render with PostgreSQL. Features full post management, social login, public profiles, comments, a contact form, and a REST API.

**Live site:** https://blog-2-hggg.onrender.com

## Features

### Posts
- Full CRUD (create, read, update, delete) for blog posts
- Draft / Published / Archived status per post
- Quick publish/unpublish toggle on post detail page (author only)
- Paginated post list (6 posts per page)
- Post tags (comma-separated, displayed as badges)
- Word count displayed on post cards
- Full-text search across post titles, subtitles, and body
- Status filter (staff see all statuses; non-staff see published only)
- Author-only edit and delete buttons (staff can also edit any post)
- Open Graph meta tags on post detail pages for social sharing

### Comments
- Logged-in users can comment on any post
- Comments display author avatar, name, and date
- Managed via Django admin

### User Accounts & Profiles
- Registration, login, logout, password change and reset
- GitHub OAuth (social login via django-allauth)
- Public profile page per user: avatar, bio, GitHub/LinkedIn/website links, published posts
- Profile edit: avatar upload, bio, social links
- "Edit Profile" button visible only when viewing your own profile

### Contact
- Contact form (name, email, subject, message) sends directly to site owner Gmail
- No public email address exposed — visitors use the form only
- Reply-to set to the visitor's email for easy replies

### REST API
- `/api/posts/` — list, create, update, delete posts (JWT required for write)
- `/api/users/` — list users
- `/api/token/` — obtain JWT token
- `/api/token/refresh/` — refresh JWT token

### Real-Time Notifications
- WebSocket endpoint: `ws/notifications/`
- Users receive notifications when new posts are created (Django Channels)

### Other
- Responsive dark-themed UI (Bootstrap 5.3, Bootstrap Icons)
- `robots.txt` and `sitemap.xml` auto-generated
- Whitenoise for static file serving
- Django admin with custom branding (django-admin-interface)

## Tech Stack
- Python 3.11 / Django 5.2
- PostgreSQL (production via Render) / SQLite (local dev)
- django-allauth, djangorestframework, djangorestframework-simplejwt
- Django Channels (ASGI / WebSockets)
- Bootstrap 5.3, Bootstrap Icons 1.11.3
- Whitenoise, dj-database-url, Gunicorn
- Deployed on Render

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/dallas8000-ops/BLOG-2.git
   cd BLOG-2
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy and configure environment variables:
   ```bash
   cp .env.example .env  # then edit .env with your values
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```bash
   python manage.py runserver 8001
   ```
8. Open http://127.0.0.1:8001/

## Required Environment Variables

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | `false` in production |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins |
| `DATABASE_URL` | PostgreSQL connection string (Render sets this automatically) |
| `GITHUB_CLIENT_ID` | GitHub OAuth app client ID |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret |
| `EMAIL_HOST_USER` | Gmail address for outgoing email |
| `EMAIL_HOST_PASSWORD` | Gmail App Password (not your normal password) |
| `CONTACT_EMAIL` | Address to receive contact form submissions |

## Social Authentication Setup
- In Django admin → Sites: set domain to `127.0.0.1:8001` (local) or your Render domain (production).
- In Django admin → Social Applications: add a GitHub entry with your client ID and secret, linked to the correct site.
- Create separate GitHub OAuth apps for local and production with matching callback URLs.

## Project Structure
```
config/          Django settings, root URLs, WSGI/ASGI
posts/           Post and Comment models, views, URLs, admin
accounts/        User profiles, public profile view, OAuth helpers
pages/           Home, About, Contact views
api/             REST API endpoints and serializers
notifications/   WebSocket consumers and utils (Django Channels)
templates/       HTML templates (base, posts, accounts, registration, pages)
static/          CSS and images
```

## Author
Built by Barney Gilliom ([@dallas8000-ops](https://github.com/dallas8000-ops))
