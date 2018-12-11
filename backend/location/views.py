from rest_framework import generics
from .models import *
from .serilazers import *

class ProvinceList(generics.ListAPIView):
    serializer_class = ProvinceWithTownsSerializer
    queryset = Province.objects.all()