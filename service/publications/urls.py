from django.urls import path
from .views import PublicationList, PublicationDetail, VoteView, Top10Publications, LatestPublications

urlpatterns = [
    path('publications/', PublicationList.as_view(), name='publication-list'),
    path('publications/<int:pk>/', PublicationDetail.as_view(), name='publication-detail'),
    path('vote/', VoteView.as_view(), name='vote'),
    path('top_publications/', Top10Publications.as_view(), name='top_publications'),
    path('latest_publications/', LatestPublications.as_view(), name='latest_publications'),
]