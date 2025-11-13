from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import IsBusinessProfileOrReadOnly, IsOwnerOrReadOnly
from .serializers import OfferSerializer,OfferCreateSerializer, OfferDetailSerializer
from offers_app.models import Offer,OfferDetail



class OfferListCreateView(generics.ListCreateAPIView):

    ordering_fields = ['min_delivery_time', 'min_price']
    search_fields = ['title', 'description']
    queryset = Offer.objects.all().order_by('-updated_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [ IsBusinessProfileOrReadOnly()]
        return [AllowAny()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferSerializer


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferCreateSerializer
        return OfferSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [ IsAuthenticated()]
        return [IsOwnerOrReadOnly()]
    
class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer