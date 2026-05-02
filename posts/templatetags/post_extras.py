import markdown as _md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def markdownify(value):
    """Convert a markdown string to safe HTML."""
    extensions = ["fenced_code", "tables", "nl2br", "sane_lists"]
    return mark_safe(_md.markdown(value or "", extensions=extensions))


@register.filter
def reading_time(value):
    """Return estimated reading time in minutes (200 wpm)."""
    words = len((value or "").split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"
