<script lang="ts" setup>
import {QCard} from 'quasar';
import EquipmentDetail from 'components/EquipmentDetail.vue';
import {PropType, defineProps, ref, Ref} from 'vue';

const props = defineProps(
  {
    character: {
      type: Object as PropType<Character>,
      required: true,
    },
  }
)
const character = ref<CharacterDetail>(getCharacterDetail(props.character));
type Term = {
  value: number,
  evaluation: number,
  level: number,
}

type Equipment = {
  id: number,
  level: number,
  name: string,
  attack: Term,
  attack_percent: Term,
  defense: Term,
  defense_percent: Term,
  health: Term,
  health_percent: Term,
  critical_rate: Term,
  critical_damage: Term
}

type Character = {
  id: number,
  name: string,
  level: number,
  birth: Date,
  attack: number,
  defense: number,
  health: number,
  critical_rate: number,
  critical_damage: number,
  card: QCard | null,
  equipments: Equipment[],
}
type CharacterDetail = Character & {
  extra_attack: number,
  base_attack_color: string,
  attack_color: string,
  extra_attack_color: string,
  extra_defense: number,
  base_defense_color: string,
  defense_color: string,
  extra_defense_color: string,
  extra_health: number,
  base_health_color: string,
  health_color: string,
  extra_health_color: string,
}
function getCharacterDetail(character: Character): CharacterDetail {
  const characterDetail = {...character} as CharacterDetail;
  characterDetail.extra_attack = 0;
  characterDetail.attack_color = 'text-white';
  characterDetail.extra_attack_color = 'text-orange';
  characterDetail.extra_defense = 0;
  characterDetail.defense_color = 'text-white';
  characterDetail.extra_defense_color = 'text-orange';
  characterDetail.extra_health = 0;
  characterDetail.health_color = 'text-white';
  characterDetail.extra_health_color = 'text-orange';
  for (const equipment of character.equipments) {
    characterDetail.attack += equipment.attack.value;
    characterDetail.defense += equipment.defense.value;
    characterDetail.health += equipment.health.value;
    characterDetail.critical_rate += equipment.critical_rate.value;
    characterDetail.critical_damage += equipment.critical_damage.value;
  }
  for (const equipment of character.equipments) {
    characterDetail.extra_attack += equipment.attack_percent.value * characterDetail.attack / 100;
    characterDetail.extra_defense += equipment.defense_percent.value * characterDetail.defense / 100;
    characterDetail.extra_health += equipment.health_percent.value * characterDetail.health / 100;
  }
  return characterDetail;
}
type EquipmentDetailConfig = {
  equipment: Equipment,
  close: () => void,
  open: () => void,
  show: boolean,
}
const equipmentDetailConfig: Ref<EquipmentDetailConfig> = ref({
  equipment: {} as Equipment,
  close: () => {
    equipmentDetailConfig.value.show = false;
  },
  open: () => {
    equipmentDetailConfig.value.show = true;
  },
  show: false,
})
type LevelColor = {
  level: number
  color: string,
}
const levelColors: LevelColor[] = [
  {level: 0, color: 'text-grey'},
  {level: 1, color: 'text-grey-8'},
  {level: 2, color: 'text-green'},
  {level: 3, color: 'text-green-8'},
  {level: 4, color: 'text-blue'},
  {level: 5, color: 'text-blue-8'},
  {level: 6, color: 'text-purple'},
  {level: 7, color: 'text-purple-8'},
  {level: 8, color: 'text-orange'},
  {level: 9, color: 'text-orange-8'},
  {level: 10, color: 'text-red'},
]
</script>

<template>
  <q-dialog v-model="equipmentDetailConfig.show"  persistent>
    <EquipmentDetail :close="equipmentDetailConfig.close" :equipment="equipmentDetailConfig.equipment"/>
  </q-dialog>
  <q-card class="q-ma-md">
    <q-card-section>
      <q-item>
        <q-item-section>
          <q-item-label>{{ character.name }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-card-section>
    <q-card-section>
      <q-item>
        <q-item-section>
          <q-item-label>等级</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-item-label>{{ character.level }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label>生命值</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-item-label>
            {{ character.health + character.extra_health}}
            <q-tooltip>
              <span :class="character.health_color">{{ character.health }}</span>
              +
              <span :class="character.extra_health_color">
                {{ character.extra_health }}
              </span>
            </q-tooltip>
          </q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label>攻击力</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-item-label>
            {{ character.attack + character.extra_attack}}
            <q-tooltip>
              <span :class="character.attack_color">{{ character.attack }}</span>
              +
              <span :class="character.extra_attack_color">
                {{ character.extra_attack }}
              </span>
            </q-tooltip>
          </q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label>防御力</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-item-label>
            {{ character.defense + character.extra_defense}}
            <q-tooltip>
              <span :class="character.defense_color">{{ character.defense }}</span>
              +
              <span :class="character.extra_defense_color">
                {{ character.extra_defense }}
              </span>
            </q-tooltip>
          </q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label>暴击率</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-item-label>{{ character.critical_rate }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label>暴击伤害</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-item-label>{{ character.critical_damage }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label>装备</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-list >
            <q-item v-for="equipment in character.equipments" :key="equipment.id" clickable v-ripple @click="equipmentDetailConfig.equipment = equipment;
                             equipmentDetailConfig.open()" :class="levelColors[equipment.level].color ">
              {{ equipment.name }}
            </q-item>
          </q-list>
        </q-item-section>
      </q-item>
    </q-card-section>
  </q-card>
</template>

<style scoped>

</style>
