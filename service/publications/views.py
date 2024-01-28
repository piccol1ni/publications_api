from rest_framework import generics, permissions
from .models import Publication, Vote
from .serializers import PublicationSerializer, VoteSerializer
from django.db import transaction


class PublicationList(generics.ListCreateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(author=self.request.user)
        except Publication.DoesNotExist:
            pass

class PublicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated]

class VoteView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        publication_id = self.request.data.get('publication')
        try:
            with transaction.atomic():
                publication = Publication.objects.get(id=publication_id)
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
        except Publication.DoesNotExist:
            pass
        
class Top10Publications(generics.ListAPIView):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all().order_by('-rating')[:10]
    
class LatestPublications(generics.ListAPIView):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all().order_by('-pub_date')[:10]