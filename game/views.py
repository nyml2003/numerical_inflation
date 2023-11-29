import json
import os

from django.http import JsonResponse

import play.settings as settings
from .core import create_character, INITIAL_CHARACTER_COUNT
from .model import CharacterInstance, CharacterPrototype, EquipmentInstance, EquipmentPrototype
from .serializer import CharacterInstanceSerializer


# Create your views here.
def init(request):
    CharacterInstance.objects.all().delete()
    CharacterPrototype.objects.all().delete()
    EquipmentInstance.objects.all().delete()
    EquipmentPrototype.objects.all().delete()
    # 初始化角色
    filename = os.path.join(settings.STATIC_URL, "equipments.json")
    with open(filename, "r", encoding="utf-8") as f:
        equipments = json.load(f)
        for equipment in equipments:
            EquipmentPrototype.objects.create(
                name=equipment.get("name")
            )
    # 初始化装备
    filename = os.path.join(settings.STATIC_URL, "characters.json")
    with open(filename, "r", encoding="utf-8") as f:
        characters = json.load(f)
        for character in characters:
            CharacterPrototype.objects.create(
                name=character.get("name")
            )
    for i in range(INITIAL_CHARACTER_COUNT):
        create_character()
    return JsonResponse(
        CharacterInstanceSerializer(CharacterInstance.objects.all(), many=True).data,
        safe=False
    )


def get_character_list(request):
    return JsonResponse(
        CharacterInstanceSerializer(CharacterInstance.objects.all(), many=True).data,
        safe=False
    )


def get_character_random(request, count):
    return JsonResponse(
        CharacterInstanceSerializer(CharacterInstance.objects.order_by("?").all()[:count], many=True).data,
        safe=False
    )
