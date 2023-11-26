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

    filename = os.path.join(settings.STATIC_URL, 'roles.json')
    with open(filename, 'r', encoding='utf-8') as f:
        roles = json.load(f)
        roles = random.sample(roles, len(roles))[0:8]
        for role in roles:
            Role.objects.create(
                name=role.get('name'),
            )
    filename = os.path.join(settings.STATIC_URL, 'equipments.json')
    with open(filename, 'r', encoding='utf-8') as f:
        equipments = json.load(f)
        equipments = random.sample(equipments, len(equipments))
        for equipment in equipments:
            Equipment.objects.create(
                name=equipment.get('name'),
            )
    # 随机分配装备
    for role in Role.objects.all():
        for equipment in random.sample(equipments, len(equipments))[0:2]:
            equipment_prototype = Equipment.objects.get(name=equipment.get('name'))
            equipment_instance = EquipmentEntity.objects.create(
                equipment_prototype=equipment_prototype,
            )
            equipment_instance.level_up()
            role.equipments.add(equipment_instance)
    return HttpResponse("初始化成功")


def get_role_list(request):
    return JsonResponse(
        RoleSerializer(Role.objects.all(), many=True).data,
        safe=False
    )


def get_fight_couple(request):
    roles = Role.objects.order_by('?')[0:2]
    return JsonResponse(
        RoleSerializer(roles, many=True).data,
        safe=False
    )