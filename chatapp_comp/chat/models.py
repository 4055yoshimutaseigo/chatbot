from django.db import models


class Message(models.Model):
    contents = models.CharField(max_length=80)
    response = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.contents
