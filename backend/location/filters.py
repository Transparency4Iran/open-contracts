import rest_framework_filters as filters
from .models import *


class ProvinceFilter(filters.FilterSet):
    class Meta:
        model = Province
        fields = {
            'name': '__all__',
            'id': '__all__',
        }


class TownFilter(filters.FilterSet):
    name = filters.AllLookupsFilter(name='name')
    province = filters.RelatedFilter(ProvinceFilter, queryset=Province.objects.all())

    class Meta:
        model = Town
        exclude = {
        }


class CityFilter(filters.FilterSet):
    name = filters.AllLookupsFilter(name='name')
    town = filters.RelatedFilter(TownFilter, queryset=Town.objects.all())

    class Meta:
        model = City
        exclude = {
        }
