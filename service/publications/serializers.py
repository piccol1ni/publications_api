from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Publication, Vote


class PublicationSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    class Meta:
        model = Publication
        fields = ['article', 'text', 'pub_date', 'author', 'rating', 'votes']
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['publication', 'vote_type']

    def validate_vote_type(self, value):
        # Проверка, что тип голоса является допустимым
        if value not in [1, -1]:
            raise serializers.ValidationError("Invalid vote type.")
        return value