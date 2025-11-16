from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsBusinessProfileOrReadOnly, IsOwnerOrReadOnly
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer
from offers_app.models import Offer, OfferDetail
from django.db.models import Min


class OfferListCreateView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    ordering_fields = ['annotated_min_price', 'annotated_min_delivery_time']
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsBusinessProfileOrReadOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferSerializer

    def get_queryset(self):
        return Offer.objects.annotate(
            annotated_min_price=Min("details__price"),
            annotated_min_delivery_time=Min("details__delivery_time_in_days")
        )


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferCreateSerializer
        return OfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsOwnerOrReadOnly()]


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
