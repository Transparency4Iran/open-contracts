from .models import *
from omid_utils.standard import standard_persian


def get_or_create_location(province, town, city):
    if not province or not town or not city:
        return None
    province = standard_persian(province)
    town = standard_persian(town)
    city = standard_persian(city)
    province, created = Province.objects.get_or_create(name=province)
    town, created = Town.objects.get_or_create(name=town, province=province)
    city, created = City.objects.get_or_create(name=city, town=town)
    return city
