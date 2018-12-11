from rest_framework import serializers
from .models import *


class BudgetInOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('year', 'amount')
        model = Budget


class OrganizationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'display_name')
        model = Organization


class PathOnlyOrganizationSerializer(serializers.ModelSerializer):
    path = OrganizationNestedSerializer(many=True)

    class Meta:
        fields = ('path',)
        model = Organization


class DetailOrganizationSerializer(serializers.ModelSerializer):
    path = OrganizationNestedSerializer(many=True)
    budgets = BudgetInOrganizationSerializer(many=True)

    class Meta:
        fields = ('path', 'budgets')
        model = Organization


class TopOrganizationSerializer(serializers.ModelSerializer):
    leaves = PathOnlyOrganizationSerializer(many=True)

    class Meta:
        fields = ('id', 'display_name', 'leaves')
        model = Organization


class TopOrganizationStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'display_name', 'contracts_count', 'errors_count')
        model = Organization


class PeopleNestedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'display_name')
        model = People


class PeopleStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'display_name', 'contracts_count', 'errors_count')
        model = People


class ExecutorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = Executor


class ExecutorListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    from location.serilazers import ProvinceNestedSerializer
    provinces = ProvinceNestedSerializer(many=True)
    top_organizations = OrganizationNestedSerializer(many=True)
    count = serializers.IntegerField()
    sum = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'provinces', 'top_organizations', 'count', 'sum')
        model = Executor


class ChildOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('display_name', 'id', 'implicit_sum', 'implicit_count')
        model = Organization
