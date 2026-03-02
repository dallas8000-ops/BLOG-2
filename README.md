# BLOG-2

A professional Django blog application with full CRUD functionality, user authentication, and presentational UI.

## Features
- Create, Read, Update, and Delete (CRUD) for blog posts
- User authentication (login, logout, signup)
- Views for archived and drafted posts
- Responsive, modern Bootstrap-based UI
- Validation and error handling

## Screenshots
- Main screen (posts list)
- Post creation/editing
- Validation/error state

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
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Project Structure
- `posts/` - Blog post app (models, views, templates)
- `accounts/` - User authentication
- `templates/` - HTML templates
- `static/` - CSS, images, JS

## Author
- Dallas8000-ops

---
This project is for educational and portfolio purposes.
