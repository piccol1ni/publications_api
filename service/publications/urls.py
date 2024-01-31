from django.urls import path
from .views import PublicationList, VoteView, DeleteVote

urlpatterns = [
    path('publications/', PublicationList.as_view(), name='publication-list'),
    path('vote/', VoteView.as_view(), name='vote'),
    path('delete_vote/<int:publication_id>', DeleteVote.as_view(), name='delete_vote'),
]