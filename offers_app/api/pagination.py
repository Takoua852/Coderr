from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


class DefaultPagination(PageNumberPagination):
    """
    Default pagination class for API views.

    Provides paginated responses with a default page size and
    allows clients to customize page size up to a maximum limit.
    """

    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100
    

    def get_page_size(self, request):
        page_size_param = request.query_params.get(self.page_size_query_param)

        if page_size_param is not None:
            try:
                page_size = int(page_size_param)
                if page_size <= 0:
                    raise ValidationError(
                        "page_size must be a positive integer.")
            except ValueError:
                raise ValidationError("page_size must be an integer.")
            return min(page_size, self.max_page_size)
        
        return self.page_size
