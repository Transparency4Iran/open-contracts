import rest_framework_filters as filters
from .models import *
from location.filters import CityFilter, City
from org.filters import *


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'title': '__all__',
            'id': '__all__',
        }


class GeneralRuleFilter(filters.FilterSet):
    class Meta:
        model = GeneralRule
        fields = {
            'title': '__all__',
            'id': '__all__',
        }


class CreditSourceFilter(filters.FilterSet):
    class Meta:
        model = CreditSource
        fields = {
            'title': '__all__',
            'id': '__all__',
        }


class ContractFilter(filters.FilterSet):
    contract_date = filters.AllLookupsFilter(name='contract_date')
    end_date = filters.AllLookupsFilter(name='end_date')
    id = filters.AllLookupsFilter(name='id')
    price = filters.AllLookupsFilter(name='price')
    title = filters.AllLookupsFilter(name='title')
    jalali_year = filters.AllLookupsFilter(name='jalali_year')
    jalali_month = filters.AllLookupsFilter(name='jalali_month')
    jalali_day = filters.AllLookupsFilter(name='jalali_day')
    duration__gte = filters.NumberFilter(name='duration', lookup_expr='gte')
    duration__lte = filters.NumberFilter(name='duration', lookup_expr='lte')
    category = filters.RelatedFilter(CategoryFilter, queryset=Category.objects.all())
    credit_source = filters.RelatedFilter(CreditSourceFilter, queryset=CreditSource.objects.all())
    general_rule = filters.RelatedFilter(GeneralRuleFilter, queryset=GeneralRule.objects.all())
    city = filters.RelatedFilter(CityFilter, queryset=City.objects.all())
    organization = filters.RelatedFilter(OrganizationFilter, queryset=Organization.objects.all())
    top_organization = filters.RelatedFilter(OrganizationFilter, queryset=Organization.objects.all())
    executor = filters.RelatedFilter(ExecutorFilter, queryset=Executor.objects.all())
    registrar = filters.RelatedFilter(PeopleFilter, queryset=People.objects.all())

    class Meta:
        model = Contract
        exclude = {

        }
