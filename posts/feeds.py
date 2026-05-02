from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse

from .models import Post


class LatestPostsFeed(Feed):
    title = "Barney Gilliom Dev Blog"
    link = "/posts/"
    description = "Latest published posts from Barney Gilliom."

    def items(self):
        return (
            Post.objects.select_related("status", "author")
            .filter(status__name__iexact="published")
            .order_by("-created_on")[:20]
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 40)

    def item_link(self, item):
        return reverse("post_detail", kwargs={"pk": item.pk})
