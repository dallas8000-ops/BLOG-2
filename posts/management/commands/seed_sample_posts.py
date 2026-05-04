from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from posts.models import Post, Status


SAMPLE_POSTS = [
    {
        "title": "Kristie Store — Production E-Commerce Platform",
        "subtitle": "Full-stack Django + React storefront deployed on Render",
        "tags": "python,django,react,postgresql,ci/cd",
        "body": (
            "A full-stack production e-commerce platform built as sole developer.\n\n"
            "Live URL: https://kristie-store.onrender.com\n\n"
            "Stack: Django REST API backend, React/TypeScript frontend, PostgreSQL database, "
            "GitHub Actions CI/CD pipeline, deployed on Render.\n\n"
            "Highlights:\n"
            "- Role-based access control (customers vs. admins)\n"
            "- JWT authentication with token refresh\n"
            "- Responsive product catalog with cart and checkout flow\n"
            "- Automated deployment on every push to main\n"
            "- Zero-downtime production configuration with WhiteNoise and gunicorn"
        ),
    },
    {
        "title": "Django REST Blog API — This Platform",
        "subtitle": "RESTful blog with JWT auth, RBAC, and full test coverage",
        "tags": "python,django,rest-api,jwt,unittest",
        "body": (
            "The platform you are reading right now. Built as a portfolio-grade Django application.\n\n"
            "GitHub: https://github.com/dallas8000-ops/BLOG-2\n\n"
            "Stack: Django 5, Django REST Framework, SimpleJWT, PostgreSQL (production), "
            "SQLite (local), Channels (WebSocket), WhiteNoise, deployed on Render.\n\n"
            "Highlights:\n"
            "- Full CRUD for posts and comments via DRF\n"
            "- JWT + session dual authentication\n"
            "- Role-based visibility (staff sees drafts, public sees published only)\n"
            "- 34 automated tests covering views, models, auth, and access control\n"
            "- Inline PDF resume viewer using PDF.js\n"
            "- Atom/RSS feed and sitemap.xml"
        ),
    },
    {
        "title": "PC Checker — Windows Diagnostics Tool",
        "subtitle": "Desktop app with FastAPI local server, charts, and PDF export",
        "tags": "python,fastapi,customtkinter,sqlite,powershell",
        "body": (
            "A product-shaped Windows desktop diagnostic application.\n\n"
            "GitHub: https://github.com/dallas8000-ops/PC-Checker\n\n"
            "Stack: Python, CustomTkinter (multi-tab GUI), FastAPI (local HTTP server), "
            "SQLite (metric sampling), Matplotlib (charts), PowerShell/WMI (system data).\n\n"
            "Highlights:\n"
            "- Background threading keeps the UI non-blocking during scans\n"
            "- UAC-aware relaunch for elevated diagnostics\n"
            "- Browser dashboard served by a local FastAPI instance\n"
            "- Export to JSON, HTML, and PDF from a single click\n"
            "- Optional read-only cloud mirror hosted on Render"
        ),
    },
    {
        "title": "FrontLine Digital — Production Marketing Platform",
        "subtitle": "React/TypeScript SPA with GitHub Actions CI/CD",
        "tags": "react,typescript,nodejs,github-actions,render",
        "body": (
            "A production business marketing platform built as sole developer.\n\n"
            "Live URL: https://gilliomfrontlinedigital.onrender.com\n"
            "GitHub: https://github.com/dallas8000-ops/FrontLineDigital\n\n"
            "Stack: React, TypeScript, Node.js, GitHub Actions, deployed on Render.\n\n"
            "Highlights:\n"
            "- Fully responsive multi-page SPA component structure\n"
            "- Dynamic UI with animated section transitions\n"
            "- Automated zero-touch deployment via GitHub Actions on every merge\n"
            "- Production-hardened build config (Vite, tree-shaking, asset hashing)"
        ),
    },
    {
        "title": "React Product Catalog — Component Library with Jest Tests",
        "subtitle": "Accessible, modular UI components with full test coverage",
        "tags": "react,typescript,jest,vite,accessibility",
        "body": (
            "A modular React/TypeScript component library with comprehensive Jest test suite.\n\n"
            "Live URL: https://react-store-catalog-1.onrender.com\n"
            "GitHub: https://github.com/dallas8000-ops/React-Store-Catalog\n\n"
            "Stack: React, TypeScript, Jest, Vite.\n\n"
            "Highlights:\n"
            "- Unit tests covering rendering, user interaction, and edge cases\n"
            "- Modal behavior, multi-criteria filter logic, keyboard navigation\n"
            "- ARIA-compliant accessible components throughout\n"
            "- Hot module replacement dev experience via Vite"
        ),
    },
]


class Command(BaseCommand):
    help = "Seed sample posts for portfolio/demo environments"

    def add_arguments(self, parser):
        parser.add_argument(
            "--author",
            dest="author",
            default="",
            help="Username to assign as author (defaults to first superuser or first user).",
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        author_username = (options.get("author") or "").strip()

        if author_username:
            try:
                author = user_model.objects.get(username=author_username)
            except user_model.DoesNotExist as exc:
                raise CommandError(f"Author '{author_username}' was not found.") from exc
        else:
            author = user_model.objects.filter(is_superuser=True).first() or user_model.objects.first()

        if not author:
            raise CommandError("No users exist. Create a user first, then run this command again.")

        published_status, _ = Status.objects.get_or_create(
            name="published",
            defaults={"description": "Visible on the main blog list."},
        )

        created_count = 0
        for entry in SAMPLE_POSTS:
            post, created = Post.objects.get_or_create(
                title=entry["title"],
                defaults={
                    "subtitle": entry["subtitle"],
                    "body": entry["body"],
                    "tags": entry.get("tags", ""),
                    "author": author,
                    "status": published_status,
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {post.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipped (exists): {post.title}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete. Created {created_count} post(s) for author '{author.username}'."
            )
        )
