from rest_framework import generics, viewsets
from .models import *
from .serilazers import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from django.db.models import Count, Sum
from rest_framework.filters import OrderingFilter


class TopOrganizationsWithLeaves(generics.ListAPIView):
    serializer_class = TopOrganizationSerializer
    queryset = Organization.objects.filter(father__isnull=True)


class TopOrganizationsStatistics(generics.ListAPIView):
    serializer_class = TopOrganizationStatisticsSerializer
    queryset = Organization.objects.filter(father__isnull=True)


class OrganizationView(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = OrganizationFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ChildOrganizationSerializer
        return DetailOrganizationSerializer


#
# class ExecutorList(generics.ListAPIView):
#     serializer_class = ExecutorNestedSerializer
#     queryset = Executor.objects.all()


class ExecutorView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExecutorListSerializer
    queryset = Executor.objects.annotate(count=Count('contracts'), sum=Sum('contracts__price'))
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = ExecutorFilter
    ordering_fields = '__all__'


class PeopleList(generics.ListAPIView):
    queryset = People.objects.all()
    serializer_class = PeopleNestedSerializer


class PeopleListWithStatistics(generics.ListAPIView):
    queryset = People.objects.all()
    serializer_class = PeopleStatisticsSerializer
