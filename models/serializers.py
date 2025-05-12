from rest_framework import serializers
from .models import GeneratedModel

class GeneratedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedModel
        fields = ['id', 'name', 'description', 'file', 'likes']
