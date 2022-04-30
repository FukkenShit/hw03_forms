"""Вспомогательные функции."""
from django.core.paginator import Paginator


def get_page_obj(request, posts, posts_per_page: int):
    """Возвращает объект page_obj для списока постов."""
    paginator = Paginator(posts, posts_per_page)
    return paginator.get_page(request.GET.get('page'))
