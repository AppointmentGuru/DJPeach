from django.http import Http404
from rest_framework import routers, serializers, viewsets, filters

from .models import Transaction

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Return only objects owned by the current user
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner_id=request.user.id)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        ordering = ('-created_date',)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_date')
    serializer_class = TransactionSerializer

    filter_backends = (IsOwnerFilterBackend,)


router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)
