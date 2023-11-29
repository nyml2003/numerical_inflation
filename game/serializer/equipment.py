from rest_framework import serializers
from game.model import EquipmentInstance


class EquipmentInstanceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    attack = serializers.SerializerMethodField()
    attack_percent = serializers.SerializerMethodField()
    defense = serializers.SerializerMethodField()
    defense_percent = serializers.SerializerMethodField()
    health = serializers.SerializerMethodField()
    health_percent = serializers.SerializerMethodField()
    critical_rate = serializers.SerializerMethodField()
    critical_damage = serializers.SerializerMethodField()

    class Meta:
        model = EquipmentInstance
        fields = (
            'id',
            'name',
            'level',
            'attack',
            'defense',
            'health',
            'critical_rate',
            'critical_damage',
            'attack_percent',
            'defense_percent',
            'health_percent',
        )

    def get_name(self, obj):
        return obj.prototype.name

    def get_level(self, obj):
        return obj.get_level()

    def get_attack(self, obj):
        return obj.eval_attack()

    def get_attack_percent(self, obj):
        return obj.eval_attack_percent()

    def get_defense(self, obj):
        return obj.eval_defense()

    def get_defense_percent(self, obj):
        return obj.eval_defense_percent()

    def get_health(self, obj):
        return obj.eval_health()

    def get_health_percent(self, obj):
        return obj.eval_health_percent()

    def get_critical_rate(self, obj):
        return obj.eval_critical_rate()

    def get_critical_damage(self, obj):
        return obj.eval_critical_damage()

