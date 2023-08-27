from rest_framework import serializers
from . import models


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Relation
        fields = "__all__"
