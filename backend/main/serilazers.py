from rest_framework import serializers
from .models import *
from location.serilazers import CitySerializer
from org.serilazers import OrganizationNestedSerializer, ExecutorNestedSerializer, PeopleNestedSerializer


class GeneralRuleListSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('id', 'title')
        model=GeneralRule



class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('id', 'title')
        model=Category


class CreditSourceListSerializer(serializers.ModelSerializer):
    class Meta:
        fields=('id', 'title')
        model=CreditSource


class ContractSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    general_rule = serializers.StringRelatedField()
    credit_source = serializers.StringRelatedField()
    city = CitySerializer()
    organizations = OrganizationNestedSerializer(many=True)
    executor = ExecutorNestedSerializer()
    registrar = PeopleNestedSerializer()
    duration=serializers.IntegerField()

    class Meta:
        fields = ('id', 'title', 'price', 'contract_date', 'code', 'contract_number',
                  'category', 'general_rule', 'credit_source', 'link', 'city', 'organizations',
                  'executor', 'registrar', 'end_date','duration','error_displays','fetch_date')
        model = Contract
