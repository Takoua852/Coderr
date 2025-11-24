from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsBusinessProfileOrReadOnly, IsOwnerOrReadOnly
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer,OfferUpdateSerializer
from offers_app.models import Offer, OfferDetail
from django.db.models import Min
from .pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import OfferFilter
from rest_framework.exceptions import ValidationError, NotFound


def validate_int_param(request, param_name):
    value = request.query_params.get(param_name)
    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        raise ValidationError(
            {param_name: f"{param_name} must be an integer."})


class OfferListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all offers or creating a new offer.

    Features:
    - Filtering by maximum delivery time (OfferFilter)
    - Searching by title or description
    - Ordering by updated_at, min_price, or min_delivery_time
    - Pagination with DefaultPagination
    - Different serializers and permissions for POST vs GET
    """
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['updated_at', 'min_price', 'min_delivery_time']
    search_fields = ['title', 'description']
    filterset_class = OfferFilter
    pagination_class = DefaultPagination

    def get_permissions(self):
        """
        Return different permissions depending on HTTP method.
        - POST: Only business users can create offers
        - GET: Any user can view the list
        """
        if self.request.method == 'POST':
            return [IsBusinessProfileOrReadOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        """
        Use different serializers depending on HTTP method.
        - POST: OfferCreateSerializer (handles nested details)
        - GET: OfferSerializer (read-only representation)
        """
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferSerializer

    def get_queryset(self):
        """
        Annotate each offer with min_price and min_delivery_time
        from related OfferDetail objects.
        """

        queryset = Offer.objects.all().annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        ).order_by('-created_at')

        creator_id = validate_int_param(self.request, "creator_id")
        min_price =  validate_int_param(self.request, "min_price")
        max_delivery_time = validate_int_param(self.request, "max_delivery_time")

        if creator_id:
            queryset = queryset.filter(user__id=creator_id)
        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)
        if max_delivery_time:
            queryset = queryset.filter(
                min_delivery_time__lte=max_delivery_time)
        return queryset


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a single offer.

    Features:
    - Uses OfferCreateSerializer for updates (PUT/PATCH) to handle nested details
    - Uses OfferSerializer for read-only representation
    - Permissions:
        - Only owners can update or delete
        - Authenticated users can read
    """
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()


    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OfferUpdateSerializer
        return OfferSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Offer.objects.all().annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )
    def get_object(self):
        try:
            obj = Offer.objects.get(pk=self.kwargs['pk'])
        except Offer.DoesNotExist:
            raise NotFound("Offer not found.")
        self.check_object_permissions(self.request, obj)
        return obj

class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """
    API view for retrieving a single OfferDetail instance.

    Permissions:
    - Only authenticated users can access
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
