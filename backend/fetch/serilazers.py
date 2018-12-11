from rest_framework import serializers
from .models import *


class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('new_count', 'yesterday', 'with_errors_count')
        model = Attempt
