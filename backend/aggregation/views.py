from rest_framework import generics, views, response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from main.filters import ContractFilter
from main.models import Contract
from org.models import Executor, Organization
from .serilazers import *
from .filters import *


class OrganizationYear(generics.ListAPIView):
    queryset = Contract.objects.values('top_organization_id', 'top_organization__name', 'jalali_year').annotate(
        count=Count('id'), sum=Sum('price'))
    serializer_class = TopOrganizationYearSerializer


class OrganizationMonth(generics.ListAPIView):
    queryset = Contract.objects.values('top_organization_id', 'top_organization__name', 'jalali_year',
                                       'jalali_month').annotate(
        count=Count('id'), sum=Sum('price'))
    serializer_class = TopOrganizationMonthSerializer


class OnProvince(generics.ListAPIView):
    queryset = Contract.objects.values('city__town__province__name', 'city__town__province__id').annotate(
        count=Count('id'), sum=Sum('price'))
    serializer_class = OnProvinceSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ContractFilter


class OnCity(generics.ListAPIView):
    queryset = Contract.objects.values('city_id').annotate(
        count=Count('id'), sum=Sum('price'))
    serializer_class = OnCitySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ContractFilter


class OnTown(generics.ListAPIView):
    queryset = Contract.objects.values('city__town_id').annotate(
        count=Count('id'), sum=Sum('price'))
    serializer_class = OnTownSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ContractFilter


class DailyFetchPerTopOrganizationView(generics.ListAPIView):
    queryset = DailyFetchPerTopOrganization.objects.all()
    serializer_class = DailyFetchPerTopOrganizationSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = DailyFetchPerTopOrganizationFilter


class ErrorSpectrumView(generics.ListAPIView):
    queryset = ErrorSpectrum.objects.all()
    serializer_class = ErrorSpectrumSerializer


#
# class OnExecutor(generics.ListAPIView):
#     queryset = Contract.objects.values('executor_id').annotate(
#         count=Count('id'), sum=Sum('price'))
#     serializer_class = OnExecutorSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filter_class = ContractFilter


class Percentile(views.APIView):
    def get(self, request):
        q = Contract.objects.filter(price__isnull=False).order_by('price')
        min_value = 0
        max_value = 29700000000
        step = (max_value - min_value) // 99
        ans = []
        for i in range(0, 99):
            start = (min_value + (i * step))
            end = (min_value + ((i + 1) * step))
            count = q.filter(price__gte=start).filter(price__lt=end).count()
            ans.append({
                'percentile': i + 1,
                'start': start,
                'end': end,
                'count': count
            })
        count = q.filter(price__gte=max_value).count()
        ans.append({
            'percentile': 100,
            'start': max_value,
            'end': q.last().price,
            'count': count
        })
        return response.Response(ans)


class ExecutorPercentile(views.APIView):
    def get(self, request):
        q = Executor.objects.annotate(count=Count('contracts'), sum=Sum('contracts__price')).order_by('sum')
        min_value = 0
        max_value = 19800000000
        step = (max_value - min_value) // 99
        ans = []
        for i in range(0, 99):
            start = (min_value + (i * step))
            end = (min_value + ((i + 1) * step))
            count = q.filter(sum__gte=start).filter(sum__lt=end).count()
            ans.append({
                'percentile': i + 1,
                'start': start,
                'end': end,
                'count': count
            })
        count = q.filter(sum__gte=max_value).count()
        ans.append({
            'percentile': 100,
            'start': max_value,
            'end': q.last().sum,
            'count': count
        })
        return response.Response(ans)


class StatView(views.APIView):
    def get(self, request):
        return response.Response({
            'contracts_count': Contract.objects.count(),
            'with_error_count':Contract.objects.exclude(errors__exact=0).count(),
            'executors_count': Executor.objects.count(),
            'organizations_count': Organization.objects.filter(
                id__in=Contract.objects.values_list('organization', flat=True)).count()
        })
