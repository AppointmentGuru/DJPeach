from django.http import Http404
from rest_framework import routers, serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models import Transaction, ScheduledPayment

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Return only objects owned by the current user
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner_id=request.user.id)

class IsCustomerFilterBackend(filters.BaseFilterBackend):
    """
    Return only objects owned by the current user
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(customer__owner_id=request.user.id)

class ScheduledPaymentFilterBackend(filters.FilterSet):

    from_date = django_filters.DateTimeFilter(name="scheduled_date", lookup_expr='gte')
    class Meta:
        model = ScheduledPayment
        fields = ['product', 'is_recurring', 'status', 'amount', 'currency', 'from_date']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        ordering = ('-created_date',)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_date')
    serializer_class = TransactionSerializer

    filter_backends = (IsOwnerFilterBackend,)


class ScheduledPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledPayment
        fields = '__all__'
        ordering = ('-created_date',)

class ScheduledPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScheduledPayment.objects.all().order_by('-created_date')

    serializer_class = ScheduledPaymentSerializer
    filter_backends = (
        IsCustomerFilterBackend,
        DjangoFilterBackend,
        filters.OrderingFilter,)
    filter_fields = ('product', 'scheduled_date', 'is_recurring', 'status', 'amount', 'currency',)
    ordering_fields = ('scheduled_date',)

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'scheduled-payments', ScheduledPaymentViewSet)
