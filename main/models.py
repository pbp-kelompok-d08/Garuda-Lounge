from django.db import models

class LandingPage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
