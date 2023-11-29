from django.db import models


class CharacterPrototype(models.Model):
    name = models.CharField(max_length=200)
