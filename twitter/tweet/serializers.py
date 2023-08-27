from rest_framework import serializers
from account import serilizers as account_serilizer

from twitter.tweet import models


class PostSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.Post(**validated_data)

    class Meta:
        model = models.Post
        fields = '__all__'


# class PostFollowingSerializer(serializers.ModelSerializer):
#     posts = PostSerializer(many=True, read_only=True)

#     class Meta:
#         model =
#         fields = '__all__'