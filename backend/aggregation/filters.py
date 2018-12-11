import rest_framework_filters as filters
from org.filters import *
from .models import *


class DailyFetchPerTopOrganizationFilter(filters.FilterSet):
    top_organization = filters.RelatedFilter(OrganizationFilter, queryset=Organization.objects.all())
    date = filters.AllLookupsFilter(name='date')
    count = filters.AllLookupsFilter(name='count')
    class Meta:
        model = DailyFetchPerTopOrganization
        exclude = {
        }
