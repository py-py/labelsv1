from rest_framework.pagination import PageNumberPagination

from .settings import PAGE_SIZE


class LabelPageNumberPagination(PageNumberPagination):
    page_size = PAGE_SIZE
