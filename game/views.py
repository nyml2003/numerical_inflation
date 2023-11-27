import os
import random

from django.http import HttpResponse, JsonResponse
import play.settings as settings
from game.models import Role, Equipment, EquipmentEntity, RoleSerializer
import json


# Create your views here.
def init(request):
    Role.objects.all().delete()
    Equipment.objects.all().delete()
    EquipmentEntity.objects.all().delete()
    filename = os.path.join(settings.STATIC_URL, "equipments.json")
    with open(filename, "r", encoding="utf-8") as f:
        equipments = json.load(f)
        equipments = random.sample(equipments, len(equipments))
        for equipment in equipments:
            Equipment.objects.create(
                name=equipment.get("name"),
            )
    filename = os.path.join(settings.STATIC_URL, "roles.json")
    with open(filename, "r", encoding="utf-8") as f:
        roles = json.load(f)
        roles = random.sample(roles, len(roles))[0:8]
        for role in roles:
            role_instance = Role.objects.create(
                name=role.get("name"),
            )
            for equipment in Equipment.objects.order_by("?")[0:5]:
                equipment_instance = EquipmentEntity.objects.create(
                    equipment_prototype=equipment,
                    owner=role_instance
                )
                for i in range(10):
                    equipment_instance.level_up()
    return HttpResponse("初始化成功")


def get_role_list(request):
    return JsonResponse(RoleSerializer(Role.objects.all(), many=True).data, safe=False)


def get_fight_couple(request):
    roles = Role.objects.order_by("?")[0:2]
    return JsonResponse(RoleSerializer(roles, many=True).data, safe=False)


def handle_fight(request):
    if request.method == "POST":
        data = json.loads(request.body)
        winner = Role.objects.get(id=data.get("winner"))
        loser = Role.objects.get(id=data.get("loser"))
        loser_name = loser.name
        Role.objects.filter(id=loser.id).delete()
        role = Role.objects.create(
            name=loser.name,
        )
        for equipment in EquipmentEntity.objects.filter(owner_id=winner.id).order_by("?")[0:4]:
            equipment_instance = EquipmentEntity.objects.create(
                equipment_prototype=equipment.equipment_prototype,
                owner=role
            )
            equipment_instance.level = equipment.level
            equipment_instance.attack = equipment.attack
            equipment_instance.attack_percent = equipment.attack_percent
            equipment_instance.defense = equipment.defense
            equipment_instance.defense_percent = equipment.defense_percent
            equipment_instance.health = equipment.health
            equipment_instance.health_percent = equipment.health_percent
            equipment_instance.critical_rate = equipment.critical_rate
            equipment_instance.critical_damage = equipment.critical_damage
            equipment_instance.save()
        equipment = EquipmentEntity.objects.create(
            equipment_prototype=Equipment.objects.order_by("?")[0],
            owner=role
        )
        for i in range(10):
            equipment.level_up()
        return JsonResponse(
            {
                "message": "success",
                "result": f'{loser_name}死了，{role.name}重生了'
            }
        )
