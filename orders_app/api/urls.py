"""
URLs for the Orders app.

Includes routes for:
- Listing and creating orders
- Retrieving, updating, or deleting a single order
- Counting all orders for a specific business user
- Counting completed orders for a specific business user
"""

from django.urls import path
from .views import OrderListCreateView, OrderDetailView, BusinessOrderCountView, CompletedOrderCountView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name="order-list"),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', BusinessOrderCountView.as_view(),  name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name="completed-order-count")
]
