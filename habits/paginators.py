from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class HabitPagination(LimitOffsetPagination):
    #page_size = 2
    #page_size_query_param = "page_size"
    #page_query_param = "page"
    #max_page_size = 10
    default_limit = 5
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 50
