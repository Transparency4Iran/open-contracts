from rest_framework import serializers
from .models import *


class ProvinceNestedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = Province


class TownNestedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = Town


class CitySerializer(serializers.ModelSerializer):
    town = TownNestedSerializer()
    province = ProvinceNestedSerializer()

    class Meta:
        fields = ('id', 'name', 'town', 'province', 'lat', 'lon')
        model = City


class TownSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()

    class Meta:
        fields = ('id', 'name', 'province', 'lat', 'lon')
        model = Town


class CityNestedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = City


class TownWithCitiesSerializer(serializers.ModelSerializer):
    cities = CityNestedSerializer(many=True)

    class Meta:
        fields = ('id', 'name', 'cities')
        model = Town


class ProvinceWithTownsSerializer(serializers.ModelSerializer):
    towns = TownWithCitiesSerializer(many=True)

    class Meta:
        fields = ('id', 'name', 'towns')
        model = Town
