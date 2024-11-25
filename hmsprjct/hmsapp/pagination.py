from rest_framework.pagination import PageNumberPagination

class ComplaintPagination(PageNumberPagination):
    page_size = 10  # Adjust the number of items per page
    page_size_query_param = "page_size"
    max_page_size = 100
