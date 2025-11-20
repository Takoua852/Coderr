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
    """
    API view for listing all orders or creating a new order.

    Features:
    - GET: Any authenticated user can view the list of orders
    - POST: Only customers can create a new order
    - Uses different serializers depending on the HTTP method
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        """
        Return different permissions depending on HTTP method.
        - POST: Only customer users can create orders
        - GET: Any authenticated user can view orders
        """
        if self.request.method == 'POST':
            return [IsCustomerUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """
        Use different serializers depending on HTTP method.
        - POST: OrderCreateSerializer (handles creation from OfferDetail)
        - GET: OrderSerializer (read-only representation)
        """
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a single Order instance.

    Features:
    - GET: Any authenticated user can retrieve an order
    - PATCH: Only business users can update the status of an order
    - DELETE: Only admin users can delete an order
    - Uses different serializers depending on HTTP method
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        """
        Use different serializers depending on HTTP method:
        - PATCH: OrderStatusUpdateSerializer for updating order status
        - GET or other methods: OrderSerializer (full read-only representation)
        """
        if self.request.method == 'PATCH':
            return OrderStatusUpdateSerializer
        return OrderSerializer

    def get_permissions(self):
        """
        Return different permissions depending on HTTP method:
        - PATCH: Only business owners can update
        - DELETE: Only admin users can delete
        - GET: Any authenticated user can read
        """
        if self.request.method == 'PATCH':
            return [IsBusinessOwner()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]


class BusinessOrderCountView(APIView):
    """
    API view to get the count of orders with status 'in_progress'
    for a specific business user.

    Permissions:
    - Only authenticated users can access.
    """   
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, format=None):
        """
        Retrieve the count of in-progress orders for the given business user.

        Args:
            business_user_id: ID of the business user
            request: HTTP request
            format: Optional format parameter

        Returns:
            JSON response containing {"order_count": <number>}
        """
        business_user = get_object_or_404(
            CustomUser, id=business_user_id, type="business")
        order_count = Order.objects.filter(
            business_user=business_user, status='in_progress').count()
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    API view to get the count of orders with status 'completed'
    for a specific business user.

    Permissions:
    - Only authenticated users can access.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, format=None):
        """
        Retrieve the count of completed orders for the given business user.

        Args:
            business_user_id: ID of the business user
            request: HTTP request
            format: Optional format parameter

        Returns:
            JSON response containing {"completed_order_count": <number>}
        """
        business_user = get_object_or_404(
            CustomUser, id=business_user_id, type="business")
        completed_order_count = Order.objects.filter(
            business_user=business_user, status='completed').count()
        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)
