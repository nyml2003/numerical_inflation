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
            role_instance=Role.objects.create(
                name=role.get("name"),
            )
            for equipment in Equipment.objects.order_by("?")[0:2]:
                equipment_instance=EquipmentEntity.objects.create(
                    equipment_prototype=equipment,
                    owner=role_instance
                )
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
        loser_random_equipment = EquipmentEntity.objects.filter(owner=loser).order_by("?").first()
        winner.level_up()
        winner.save()
        loser.save()
        if loser_random_equipment:
            loser_random_equipment.owner = winner
            loser_random_equipment.save()
        else:
            Role.objects.get(id=loser.id).delete()
        return HttpResponse("处理成功")
    
        
