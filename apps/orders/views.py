from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from apps.orders.filters import BuyerOrderFilter
from apps.orders.models import Order
from apps.orders.permissions import IsOwner
from apps.orders.serializers.orders import OrderReadSerializer, OrderWriteSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    http_method_names = ["get", "post", "delete"]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BuyerOrderFilter

    def get_queryset(self):
        return Order.objects.get_related_queryset(self.request.user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return OrderReadSerializer
        return OrderWriteSerializer

    @extend_schema(request=OrderWriteSerializer, responses={201: OrderReadSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=[request.data], many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(*serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
