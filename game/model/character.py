from django.db import models

from game.core import EQUIPMENT_LEVEL_LIMIT


class CharacterInstance(models.Model):
    prototype = models.ForeignKey('CharacterPrototype', on_delete=models.CASCADE)
    attack = models.FloatField(default=200)
    defense = models.FloatField(default=100)
    health = models.FloatField(default=1000)
    critical_rate = models.FloatField(default=5)
    critical_damage = models.FloatField(default=50)
    birth = models.DateTimeField(auto_now_add=True)

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_health(self):
        return self.health

    def get_critical_rate(self):
        return self.critical_rate

    def get_critical_damage(self):
        return self.critical_damage

    def level_up(self):
        equipments = self.equipments.all()
        for equipment in equipments:
            if not equipment.level_up():
                continue
            else:
                break

    def get_level(self):
        equipments = self.equipments.all()
        level = 0
        for equipment in equipments:
            level += equipment.get_level()
        return level

    def level_up_to(self, level):
        if level > EQUIPMENT_LEVEL_LIMIT * len(self.equipments.all()):
            level = EQUIPMENT_LEVEL_LIMIT * len(self.equipments.all())
        if level < self.get_level():
            return
        while self.get_level() < level:
            for equipment in self.equipments.order_by('?'):
                if not equipment.level_up():
                    continue
                else:
                    break



