import django_filters
from .models import Publication

class PublicationFilter(django_filters.FilterSet):
    class Meta:
        model = Publication
        fields = ['id', 'article', 'author__username', 'pub_date']