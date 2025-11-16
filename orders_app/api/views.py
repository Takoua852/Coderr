from rest_framework import generics
from rest_framework.views import APIView
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from orders_app.models import Order
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomerUser, IsBusinessOwner, IsAdminUser
from auth_app.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response


class OrderListCreateView(generics.ListCreateAPIView):

    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomerUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        profile = getattr(self.request.user, 'profile', None)
        if not profile:
            return Order.objects.none()
        return Order.objects.filter(
            customer_user__profile=profile
        ) | Order.objects.filter(
            business_user__profile=profile
        )


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OrderStatusUpdateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsBusinessOwner()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]


class BusinessOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, format=None):
        business_user = get_object_or_404(
            CustomUser, id=business_user_id, type="business")
        order_count = Order.objects.filter(
            business_user=business_user, status='in_progress').count()
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    def get(self, request, business_user_id, format=None):
        business_user = get_object_or_404(
            CustomUser, id=business_user_id, type="business")
        completed_order_count = Order.objects.filter(
            business_user=business_user, status='in_progress').count()
        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)
