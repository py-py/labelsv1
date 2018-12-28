from rest_framework.pagination import PageNumberPagination

from .settings import PAGINATION_PAGE_SIZE


class LabelPageNumberPagination(PageNumberPagination):
    page_size = PAGINATION_PAGE_SIZE
