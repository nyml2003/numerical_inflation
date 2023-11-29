import django.db.models as models
from game.core import Attack, AttackPercent, Defense, DefensePercent, Health, HealthPercent, CriticalRate, \
    CriticalDamage, EQUIPMENT_LEVEL_LIMIT, get_random_term
from .character import CharacterInstance
from .equipment_prototype import EquipmentPrototype


class EquipmentInstance(models.Model):
    prototype = models.ForeignKey(EquipmentPrototype, on_delete=models.CASCADE)
    attack = models.FloatField(default=0)
    attack_level = models.IntegerField(default=0)
    attack_percent = models.FloatField(default=0)
    attack_percent_level = models.IntegerField(default=0)
    defense = models.FloatField(default=0)
    defense_level = models.IntegerField(default=0)
    defense_percent = models.FloatField(default=0)
    defense_percent_level = models.IntegerField(default=0)
    health = models.FloatField(default=0)
    health_level = models.IntegerField(default=0)
    health_percent = models.FloatField(default=0)
    health_percent_level = models.IntegerField(default=0)
    critical_rate = models.FloatField(default=0)
    critical_rate_level = models.IntegerField(default=0)
    critical_damage = models.FloatField(default=0)
    critical_damage_level = models.IntegerField(default=0)
    owner = models.ForeignKey(CharacterInstance, on_delete=models.CASCADE, related_name='equipments')

    def eval_attack(self):
        return {
            'evaluation': Attack().evaluate(self.attack, self.attack_level),
            'value': self.attack,
            'level': self.attack_level
        }

    def eval_attack_percent(self):
        return {
            'evaluation': AttackPercent().evaluate(self.attack_percent, self.attack_percent_level),
            'value': self.attack_percent,
            'level': self.attack_percent_level
        }

    def eval_defense(self):
        return {
            'evaluation': Defense().evaluate(self.defense, self.defense_level),
            'value': self.defense,
            'level': self.defense_level
        }

    def eval_defense_percent(self):
        return {
            'evaluation': DefensePercent().evaluate(self.defense_percent, self.defense_percent_level),
            'value': self.defense_percent,
            'level': self.defense_percent_level
        }
    def eval_health(self):
        return {
            'evaluation': Health().evaluate(self.health, self.health_level),
            'value': self.health,
            'level': self.health_level
        }

    def eval_health_percent(self):
        return {
            'evaluation': HealthPercent().evaluate(self.health_percent, self.health_percent_level),
            'value': self.health_percent,
            'level': self.health_percent_level
        }
    def eval_critical_rate(self):
        return {
            'evaluation': CriticalRate().evaluate(self.critical_rate, self.critical_rate_level),
            'value': self.critical_rate,
            'level': self.critical_rate_level
        }

    def eval_critical_damage(self):
        return {
            'evaluation': CriticalDamage().evaluate(self.critical_damage, self.critical_damage_level),
            'value': self.critical_damage,
            'level': self.critical_damage_level
        }

    def get_level(self):
        return (
                self.attack_level
                + self.attack_percent_level
                + self.defense_level
                + self.defense_percent_level
                + self.health_level
                + self.health_percent_level
                + self.critical_rate_level
                + self.critical_damage_level
        )

    def level_up(self):
        level = self.get_level()
        if level >= EQUIPMENT_LEVEL_LIMIT:
            return False
        selected_term_name, selected_term = get_random_term()
        self.__setattr__(selected_term_name, self.__getattribute__(selected_term_name) + selected_term)
        self.__setattr__(selected_term_name + '_level', self.__getattribute__(selected_term_name + '_level') + 1)
        self.save()
        return True

    def level_up_to(self, level):
        if level <= self.get_level() or level >= 10:
            return False
        while self.get_level() < level:
            self.level_up()
        return True
