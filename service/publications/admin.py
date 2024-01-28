from django.contrib import admin

from .models import Publication, Vote

admin.site.register(Publication)
admin.site.register(Vote)
