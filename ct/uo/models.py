from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Formation(models.Model):
    intitule = models.CharField(max_length=100)
    description = models.TextField()
    responsable = models.OneToOneField(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="responsable_de_formation"
    )

    def __str__(self):
        return self.intitule

    


class UE(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    cm = models.PositiveIntegerField()
    td = models.PositiveIntegerField()
    tp = models.PositiveIntegerField()
    credits = models.PositiveIntegerField()
    formations = models.ManyToManyField(Formation, related_name="ues")
    responsables = models.ManyToManyField(User, related_name="ues_responsables")

    def __str__(self):
        return self.titre

