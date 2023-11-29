import numpy as np

from .constants import *
from game.model import EquipmentPrototype, EquipmentInstance, CharacterInstance, CharacterPrototype


def create_equipment(owner: CharacterInstance):
    EquipmentInstance.objects.create(
        prototype=EquipmentPrototype.objects.order_by("?").first(),
        owner=owner
    )


def create_character():
    character = CharacterInstance.objects.create(
        prototype=CharacterPrototype.objects.order_by("?").first()
    )
    for i in range(np.random.randint(1, CHARACTER_EQUIPMENT_LIMIT + 1)):
        create_equipment(character)
    character.level_up_to(np.random.randint(1, CHARACTER_LEVEL_LIMIT + 1))
    return
