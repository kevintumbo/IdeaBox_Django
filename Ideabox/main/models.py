from django.db import models
from django.conf import settings

# Create your models here.


class Idea(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.TextField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    idea = models.ForeignKey(Idea, related_name='comments')
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} by {1} on {2}".format(self.comment, self.user, self.idea)
