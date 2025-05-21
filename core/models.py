from djongo import models


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    finalScore = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.username
