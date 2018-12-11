import rest_framework_filters as filters
from .models import *


class OrganizationFilter(filters.FilterSet):
    father = filters.RelatedFilter('org.filters.OrganizationFilter', name='father', queryset=Organization.objects.all())

    class Meta:
        model = Organization
        fields={
            'id':'__all__',
            'name':'__all__',
            'father':['exact','isnull']
        }


class ExecutorFilter(filters.FilterSet):
    class Meta:
        model = Executor
        fields = {
            'name': '__all__',
            'id': '__all__',
        }


class PeopleFilter(filters.FilterSet):
    class Meta:
        model = People
        fields = {
            'name': '__all__',
            'id': '__all__',
        }
