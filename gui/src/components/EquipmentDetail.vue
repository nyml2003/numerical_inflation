<script setup lang="ts">
import {PropType, ref} from 'vue';
const props = defineProps(
  {
    equipment: {
      type: Object as PropType<Equipment>,
      required: true,
    },
    close: {
      type: Function as PropType<() => void>,
      required: true,
    },
  }
)
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
const equipment = ref<Equipment>(props.equipment);

type EvaluationColor = {
  level: [number, number]
  color: string,
}

const evaluationColors: EvaluationColor[] = [
  {level: [0, 40], color: 'text-grey'},
  {level: [40, 60], color: 'text-green'},
  {level: [60, 80], color: 'text-blue'},
  {level: [80, 100], color: 'text-purple'},
  {level: [100, 120], color: 'text-orange'},
  {level: [120, 140], color: 'text-red'},
]

function getEvaluaitionColor(value: number): string {
  return evaluationColors.find((color) => value >= color.level[0] && value < color.level[1])?.color ?? 'text-grey';
}

const termKeys = [
  [
    'attack',
    '攻击'
  ],
  [
    'attack_percent',
    '攻击百分比加成'
  ],
  [
    'defense',
    '防御'
  ],
  [
    'defense_percent',
    '防御百分比加成'
  ],
  [
    'health',
    '生命'
  ],
  [
    'health_percent',
    '生命百分比加成'
  ],
  [
    'critical_rate',
    '暴击率'
  ],
  [
    'critical_damage',
    '暴击伤害'
  ]
];

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

function getTotalEvaluation(): number {
  // 除以有值的项
  return (
    equipment.value.attack.evaluation +
    equipment.value.attack_percent.evaluation +
    equipment.value.defense.evaluation +
    equipment.value.defense_percent.evaluation +
    equipment.value.health.evaluation +
    equipment.value.health_percent.evaluation +
    equipment.value.critical_rate.evaluation +
    equipment.value.critical_damage.evaluation
  ) / (
    (equipment.value.attack.value > 0 ? 1 : 0) +
    (equipment.value.attack_percent.value > 0 ? 1 : 0) +
    (equipment.value.defense.value > 0 ? 1 : 0) +
    (equipment.value.defense_percent.value > 0 ? 1 : 0) +
    (equipment.value.health.value > 0 ? 1 : 0) +
    (equipment.value.health_percent.value > 0 ? 1 : 0) +
    (equipment.value.critical_rate.value > 0 ? 1 : 0) +
    (equipment.value.critical_damage.value > 0 ? 1 : 0)
  );
}
</script>

<template>
<q-card class="q-ma-md q-pa-md">
  <q-card-section>
    <q-item-label header>{{equipment.name}}</q-item-label>
  </q-card-section>
  <q-list bordered>
    <q-item>
      <q-item-section>等级</q-item-section>
      <q-item-section>{{equipment.level}}</q-item-section>
    </q-item>
    <q-item>
      <q-item-section>总评分</q-item-section>
      <q-item-section>
        <q-item-label :class="getEvaluaitionColor(getTotalEvaluation())">
          {{ (
    equipment.attack.evaluation +
    equipment.attack_percent.evaluation +
    equipment.defense.evaluation +
    equipment.defense_percent.evaluation +
    equipment.health.evaluation +
    equipment.health_percent.evaluation +
    equipment.critical_rate.evaluation +
    equipment.critical_damage.evaluation
  ).toFixed(2) }}
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item v-for="key in termKeys.filter((key) => equipment[key[0]].value > 0)" :key="key[0]">
      <q-item-section :class="levelColors[equipment[key[0]].level].color">
        {{key[1]}}
      </q-item-section>
      <q-item-section>
        <q-item-label :class="getEvaluaitionColor(equipment[key[0]].evaluation)">
          {{equipment[key[0]].value}}
        </q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
  <q-card-actions align="right">
    <q-btn label="关闭" color="primary" @click="close" />
  </q-card-actions>
</q-card>
</template>

<style scoped>

</style>
