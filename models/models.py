from django.db import models


class GeneratedModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='generated_models/')
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name





# Create your models here.
