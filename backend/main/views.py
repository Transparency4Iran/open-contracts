from .lib import read_remaining
from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import F,ExpressionWrapper,fields
from .models import *
from .filters import *
from .serilazers import *


class ContractList(viewsets.ReadOnlyModelViewSet):
    queryset = Contract.objects.annotate(duration=ExpressionWrapper(((F('end_date')-F('contract_date'))/(24*3600*1000000)),output_field=fields.IntegerField()))
    serializer_class = ContractSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ContractFilter
    ordering_fields = '__all__'
    lookup_field = 'code'


class GeneralRuleList(generics.ListAPIView):
    queryset = GeneralRule.objects.all()
    serializer_class = GeneralRuleListSerializer


class CreditSourceList(generics.ListAPIView):
    queryset = CreditSource.objects.all()
    serializer_class = CreditSourceListSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


def force_read(request):
    read_remaining()
