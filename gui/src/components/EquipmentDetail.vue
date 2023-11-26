<script setup lang="ts">
import {PropType, ref} from "vue";
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
type Equipment = {
  id: number,
  name: string,
  level: number,
  attack: number,
  attack_percent: number,
  defense: number,
  defense_percent: number,
  health: number,
  health_percent: number,
  critical_rate: number,
  critical_damage: number,
}
const equipment = ref<Equipment>(props.equipment);

</script>

<template>
<q-card class="q-ma-md">
  <q-card-section>
    <q-item-label header>{{equipment.name}}</q-item-label>
  </q-card-section>
  <q-card-section>
    <q-item-label>等级: {{equipment.level}}</q-item-label>
    <q-item-label v-if="equipment.attack">
      攻击: +{{equipment.attack.toFixed(2)}}
    </q-item-label>
    <q-item-label v-if="equipment.attack_percent">
      攻击: +{{equipment.attack_percent.toFixed(2)}}%
    </q-item-label>
    <q-item-label v-if="equipment.defense">
      防御: +{{equipment.defense.toFixed(2)}}
    </q-item-label>
    <q-item-label v-if="equipment.defense_percent">
      防御: +{{equipment.defense_percent.toFixed(2)}}%
    </q-item-label>
    <q-item-label v-if="equipment.health">
      生命: +{{equipment.health.toFixed(2)}}
    </q-item-label>
    <q-item-label v-if="equipment.health_percent">
      生命: +{{equipment.health_percent.toFixed(2)}}%
    </q-item-label>
    <q-item-label v-if="equipment.critical_rate">
      暴击率: +{{equipment.critical_rate.toFixed(2)}}%
    </q-item-label>
    <q-item-label v-if="equipment.critical_damage">
      暴击伤害: +{{equipment.critical_damage.toFixed(2)}}%
    </q-item-label>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn label="关闭" color="primary" @click="close" />
  </q-card-actions>
</q-card>
</template>

<style scoped>

</style>
