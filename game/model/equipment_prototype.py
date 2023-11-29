import django.db.models as models


class EquipmentPrototype(models.Model):
    name = models.CharField(max_length=20)
