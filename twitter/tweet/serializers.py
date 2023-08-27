from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.Post(**validated_data)

    class Meta:
        model = models.Post
        fields = "__all__"

