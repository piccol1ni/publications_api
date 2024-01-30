from rest_framework import generics, permissions
from .models import Publication, Vote
from .serializers import PublicationSerializer, VoteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .filters import PublicationFilter
from django.db import transaction


class PublicationList(generics.ListCreateAPIView):
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicationFilter

    def get_queryset(self):
        return Publication.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class VoteView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        publication_id = self.request.data.get('publication')
        publication = get_object_or_404(Publication, id=publication_id)
        vote_type = serializer.validated_data.get('vote_type')

        existing_vote = Vote.objects.filter(user=self.request.user, publication=publication).first()    
            
        if existing_vote:
            existing_vote.delete()
            publication.rating -= vote_type
            publication.votes -= 1
            
        else:
            serializer.save(user=self.request.user)
            publication.rating += vote_type
            publication.votes += 1

        publication.save()

        
class Top10Publications(generics.ListAPIView):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all().order_by('-rating')[:10]
    
class LatestPublications(generics.ListAPIView):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all().order_by('-pub_date')[:10]