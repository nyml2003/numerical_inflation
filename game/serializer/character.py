from rest_framework import serializers

from game.model import CharacterInstance
from .equipment import EquipmentInstanceSerializer


class CharacterInstanceSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    attack = serializers.SerializerMethodField()
    defense = serializers.SerializerMethodField()
    health = serializers.SerializerMethodField()
    critical_rate = serializers.SerializerMethodField()
    critical_damage = serializers.SerializerMethodField()
    equipments = serializers.SerializerMethodField()
    birth = serializers.SerializerMethodField()

    class Meta:
        model = CharacterInstance
        fields = (
            'id',
            'level',
            'name',
            'attack',
            'defense',
            'health',
            'critical_rate',
            'critical_damage',
            'equipments',
            'birth'
        )

    def get_equipments(self, obj):
        return EquipmentInstanceSerializer(obj.equipments.all(), many=True).data

    def get_birth(self, obj):
        return obj.birth

    def get_name(self, obj):
        return obj.prototype.name

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

    def get_level(self, obj):
        return obj.get_level()
