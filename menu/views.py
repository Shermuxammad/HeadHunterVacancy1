from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem
from .form import MenuItemForm
from .templatetags.treemenu_tags import _render_menu_items
from django.views.generic import TemplateView
from django.core.cache import cache


def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu/list.html', {'menu_items': menu_items})


def menu_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'menu/form.html', {'form': form})


def menu_edit(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'menu/form.html', {'form': form})


def menu_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    menu_item.delete()
    return redirect('menu_list')


class MenuView(TemplateView):
    template_name = 'treemenu/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get('name', 'main')
        cache_key = f'treemenu_{name}'
        menu_html = cache.get(cache_key)
        if not menu_html:
            menu_items = MenuItem.objects.filter(parent__isnull=True).order_by('tree_id', 'lft')
            menu_html = _render_menu_items(menu_items, name, self.request)
            cache.set(cache_key, menu_html)
        context['menu'] = menu_html
        return context
