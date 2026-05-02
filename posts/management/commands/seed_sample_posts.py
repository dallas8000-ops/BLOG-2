from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from posts.models import Post, Status


SAMPLE_POSTS = [
    {
        "title": "Kristie Store E-commerce Launch",
        "subtitle": "Project spotlight: storefront build and deployment",
        "body": (
            "I designed and deployed the Kristie Store project.\n\n"
            "Live URL: https://kristie-store.onrender.com\n\n"
            "Highlights:\n"
            "- Responsive storefront layout\n"
            "- Product-focused user experience\n"
            "- Render deployment and production configuration"
        ),
    },
    {
        "title": "Frontline Digital Site Rollout",
        "subtitle": "Project spotlight: business web presence",
        "body": (
            "I built and launched the Frontline Digital website.\n\n"
            "Live URL: https://gilliomfrontlinedigital.onrender.com\n\n"
            "Highlights:\n"
            "- Service-first information architecture\n"
            "- Clean, modern UI for client trust\n"
            "- Production hosting on Render"
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
