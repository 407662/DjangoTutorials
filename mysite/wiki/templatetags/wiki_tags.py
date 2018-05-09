import markdown
import re

from django import template

pattern = re.compile(r"\[\[([A-Za-z0-9_]+)\]\]")
register = template.Library()


@register.filter
def markup(text):
    return markdown.markdown(text)


@register.filter
def wikify(text):
    return pattern.sub(r'''<a href="/wiki/\1/">\1</a>''', text)
