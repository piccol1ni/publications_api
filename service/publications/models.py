from django.db import models
from django.contrib.auth.models import User

class Publication(models.Model):
    article = models.CharField()
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Статья : {self.article}"
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])
    
    def __str__(self):
        return f"{self.user} оценивает {self.publication}"
    
