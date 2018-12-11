from rest_framework import serializers
from .models import *
from org.serilazers import OrganizationNestedSerializer


class TopOrganizationYearSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(source='top_organization_id')
    organization_name = serializers.CharField(source='top_organization__name')
    year = serializers.IntegerField(source='jalali_year')
    count = serializers.IntegerField()
    sum = serializers.IntegerField()


class TopOrganizationMonthSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(source='top_organization_id')
    organization_name = serializers.CharField(source='top_organization__name')
    year = serializers.IntegerField(source='jalali_year')
    month = serializers.IntegerField(source='jalali_month')
    count = serializers.IntegerField()
    sum = serializers.IntegerField()


class OnProvinceSerializer(serializers.Serializer):
    province = serializers.CharField(source='city__town__province__name')
    province_id = serializers.IntegerField(source='city__town__province__id')
    count = serializers.IntegerField()
    sum = serializers.IntegerField()


class OnTownSerializer(serializers.Serializer):
    town = serializers.SerializerMethodField()
    count = serializers.IntegerField()
    sum = serializers.IntegerField()

    def get_town(self, obj):
        from location.models import Town
        from location.serilazers import TownSerializer
        if obj.get('city__town_id', None):
            town_obj = Town.objects.get(id=obj.get('city__town_id', None))
            return TownSerializer(town_obj).data
        return None


class OnCitySerializer(serializers.Serializer):
    city = serializers.SerializerMethodField()
    count = serializers.IntegerField()
    sum = serializers.IntegerField()

    def get_city(self, obj):
        from location.models import City
        from location.serilazers import CitySerializer
        if obj.get('city_id', None):
            city_obj = City.objects.get(id=obj.get('city_id', None))
            return CitySerializer(city_obj).data
        return None


#
# class OnExecutorSerializer(serializers.Serializer):
#     executor = serializers.SerializerMethodField()
#     count = serializers.IntegerField()
#     sum = serializers.IntegerField()
#
#     def get_executor(self, obj):
#         from org.models import Executor
#         from org.serilazers import ExecutorInAggregateSerializer
#         if obj.get('executor_id', None):
#             executor_obj = Executor.objects.get(id=obj.get('executor_id', None))
#             return ExecutorInAggregateSerializer(executor_obj).data
#         return None

class ErrorSpectrumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorSpectrum
        fields = ('bit', 'label', 'count')


class DailyFetchPerTopOrganizationSerializer(serializers.ModelSerializer):
    top_organization = OrganizationNestedSerializer()

    class Meta:
        model = DailyFetchPerTopOrganization
        fields = ('date', 'top_organization', 'count')
