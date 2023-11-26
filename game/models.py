import random

import numpy as np
from rest_framework import serializers
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=20)
    base_attack = models.FloatField(default=0)
    base_defense = models.FloatField(default=0)
    base_health = models.FloatField(default=0)
    base_critical_rate = models.FloatField(default=5)
    base_critical_damage = models.FloatField(default=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_attack = np.random.normal(15, 5)
        self.base_defense = np.random.normal(15, 5)
        self.base_health = np.random.normal(150, 50)

    def get_attack(self):
        return self.base_attack \
            + sum([equipment.get_attack() for equipment in EquipmentEntity.objects.filter(owner_id=self.id)]) \
            + sum([equipment.get_attack_percent(self.base_attack) for equipment in
                   EquipmentEntity.objects.filter(owner_id=self.id)])

    def get_defense(self):
        return self.base_defense \
            + sum([equipment.get_defense() for equipment in EquipmentEntity.objects.filter(owner_id=self.id)]) \
            + sum([equipment.get_defense_percent(self.base_defense) for equipment in
                   EquipmentEntity.objects.filter(owner_id=self.id)])

    def get_health(self):
        return self.base_health \
            + sum([equipment.get_health() for equipment in EquipmentEntity.objects.filter(owner_id=self.id)]) \
            + sum([equipment.get_health_percent(self.base_health) for equipment in
                   EquipmentEntity.objects.filter(owner_id=self.id)])

    def get_critical_rate(self):
        return self.base_critical_rate\
            + sum([equipment.get_critical_rate() for equipment in EquipmentEntity.objects.filter(owner_id=self.id)])

    def get_critical_damage(self):
        return self.base_critical_damage\
            + sum([equipment.get_critical_damage() for equipment in EquipmentEntity.objects.filter(owner_id=self.id)])

    def level_up(self):
        for equipment in self.equipments.all():
            if not equipment.level_up():
                continue
            else:
                break


class RoleSerializer(serializers.ModelSerializer):
    equipments = serializers.SerializerMethodField()
    attack = serializers.SerializerMethodField()
    defense = serializers.SerializerMethodField()
    health = serializers.SerializerMethodField()
    critical_rate = serializers.SerializerMethodField()
    critical_damage = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ('id', 'name', 'attack', 'defense', 'health', 'critical_rate', 'critical_damage', 'equipments')

    def get_equipments(self, obj):
        equipments = EquipmentEntity.objects.filter(owner_id=obj.id)
        return EquipmentEntitySerializer(equipments, many=True).data

    def get_attack(self, obj):
        return obj.get_attack()

    def get_defense(self, obj):
        return obj.get_defense()

    def get_health(self, obj):
        return obj.get_health()

    def get_critical_rate(self, obj):
        return obj.get_critical_rate()

    def get_critical_damage(self, obj):
        return obj.get_critical_damage()


class Equipment(models.Model):
    name = models.CharField(max_length=20)


class EquipmentEntity(models.Model):
    equipment_prototype = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    attack = models.FloatField(default=0)
    attack_percent = models.FloatField(default=0)
    defense = models.FloatField(default=0)
    defense_percent = models.FloatField(default=0)
    health = models.FloatField(default=0)
    health_percent = models.FloatField(default=0)
    critical_rate = models.FloatField(default=0)
    critical_damage = models.FloatField(default=0)
    owner = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='equipments', null=True)

    def get_attack(self):
        return self.attack

    def get_attack_percent(self, base_attack):
        return self.attack_percent * base_attack / 100

    def get_defense(self):
        return self.defense

    def get_defense_percent(self, base_defense):
        return self.defense_percent * base_defense / 100

    def get_health(self):
        return self.health

    def get_health_percent(self, base_health):
        return self.health_percent * base_health / 100

    def get_critical_rate(self):
        return self.critical_rate

    def get_critical_damage(self):
        return self.critical_damage

    def level_up(self):
        if self.level > 10:
            return False
        self.level += 1
        choices = [
            'attack',
            'attack_percent',
            'defense',
            'defense_percent',
            'health',
            'health_percent',
            'critical_rate',
            'critical_damage'
        ]
        choice = random.sample(choices, 1)[0]
        if choice == 'attack':
            self.attack += np.random.normal(15, 5)
        elif choice == 'attack_percent':
            self.attack_percent += np.random.normal(5, 1)
        elif choice == 'defense':
            self.defense += np.random.normal(15, 5)
        elif choice == 'defense_percent':
            self.defense_percent += np.random.normal(5, 1)
        elif choice == 'health':
            self.health += np.random.normal(150, 50)
        elif choice == 'health_percent':
            self.health_percent += np.random.normal(5, 1)
        elif choice == 'critical_rate':
            self.critical_rate += np.random.normal(5, 1)
        elif choice == 'critical_damage':
            self.critical_damage += np.random.normal(10, 2)
        self.save()
        return True


class EquipmentEntitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = EquipmentEntity
        fields = (
        'id', 'name', 'level', 'attack', 'attack_percent', 'defense', 'defense_percent', 'health', 'health_percent',
        'critical_rate', 'critical_damage')

    def get_name(self, obj):
        return obj.equipment_prototype.name