from rest_framework import generics, permissions, status
from rest_framework.response import Response
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
        ordering = self.request.query_params.get('ordering', '-pub_date')

        if ordering not in ['rating', 'pub_date']:
            ordering = '-pub_date'
            return Publication.objects.all().order_by(ordering)

        return Publication.objects.all().order_by(f"-{ordering}")[:10]

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
            publication.rating -= vote_type
            publication.votes -= 1
            publication.save()
        
            existing_vote.delete()
            
        serializer.save(user=self.request.user)
        publication.rating += vote_type
        publication.votes += 1
        publication.save()
        
class DeleteVote(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        publication_id = self.kwargs.get('publication_id')
        publication = get_object_or_404(Publication, id=publication_id)

        existing_vote = Vote.objects.filter(user=self.request.user, publication=publication).first()
        
        if existing_vote:
            existing_vote.delete()
            publication.rating -= existing_vote.vote_type
            publication.votes -= 1
            publication.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Vote not found"}, status=status.HTTP_404_NOT_FOUND)

    