from rest_framework import serializers

class SensiboPatchSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    newValue = serializers.CharField(max_length=10)
