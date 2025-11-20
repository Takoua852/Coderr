from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    """
    Default pagination class for API views.

    Provides paginated responses with a default page size and
    allows clients to customize page size up to a maximum limit.
    """
    page_size = 6
    max_page_size_param = 'page_size'
    max_page_size = 100