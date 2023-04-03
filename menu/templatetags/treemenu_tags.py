from django import template
from menu.models import MenuItem
from django.urls import reverse, NoReverseMatch
from bs4 import BeautifulSoup

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, name):
    request = context['request']
    menu_items = MenuItem.objects.filter(parent__isnull=True).order_by('tree_id', 'lft')
    return _render_menu_items(menu_items, name, request)


def _render_menu_items(items, name, request):
    menu_html = '<ul class="menu-%s">' % name
    for item in items:
        url = item.url
        if not url.startswith('http') and not url.startswith('/'):
            # Try to reverse URL by name
            try:
                url = reverse(url)
            except NoReverseMatch:
                pass
        active = False
        if request.path.startswith(url):
            active = True
        menu_html += '<li class="%s"><a href="%s">%s</a>' % ('active' if active else '', url, item.title)
        children = item.children.filter()
        if children.exists():
            menu_html += _render_menu_items(children, name, request)
        menu_html += '</li>'
    menu_html += '</ul>'
    menu_html.split('"')
    return menu_html
