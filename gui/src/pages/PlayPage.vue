<script setup lang="ts">
import {onMounted, ref} from 'vue';
import {api} from 'boot/axios';
import EquipmentDetail from 'components/EquipmentDetail.vue';
import {QCard, useQuasar} from 'quasar';
const $q = useQuasar();
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
type Role = {
  id: number,
  name: string,
  attack: number,
  defense: number,
  health: number,
  current_health: number,
  critical_rate: number,
  critical_damage: number,
  equipments: Equipment[],
  card: HTMLElement | null,
}
type EquipmentLevel = {
  level: number,
  color_class: string,
}
type EquipmentDetailConfig = {
  equipment: Equipment,
  showEquipmentDetail: boolean,
  open: (equipment: Equipment) => void,
  close: () => void,
}
const equipmentDetailConfig = ref<EquipmentDetailConfig>({
  equipment: {} as Equipment,
  showEquipmentDetail: false,
  open: (equipment: Equipment) => {
    equipmentDetailConfig.value.equipment = equipment;
    equipmentDetailConfig.value.showEquipmentDetail = true;
  },
  close: () => {
    equipmentDetailConfig.value.showEquipmentDetail = false;
  },
})
const equipmentLevels: EquipmentLevel[] = [
  {level: 1, color_class: 'text-green'},
  {level: 2, color_class: 'text-blue'},
  {level: 3, color_class: 'text-purple'},
  {level: 4, color_class: 'text-orange'},
]
const roles = ref<Role[]>([]);
onMounted(()=>{
  decorate_fight();
})
function calculateDamage(attack: number, defense: number, critical_rate: number, critical_damage: number) {
    const random = Math.random() * 100;
    const isCritical : boolean = random < critical_rate;
    const critical_multiplier = isCritical ? 1 + critical_damage / 100 : 1;
    const reduction_multiplier =  attack / (attack + defense);
    const random_multiplier = 1 + Math.random() * 0.2 - 0.1;
    const damage = attack * critical_multiplier * reduction_multiplier * random_multiplier;
    return {
        isCritical,
        damage,
    }
}
function shake(element: HTMLElement  ) {
    if (element instanceof HTMLElement) {
        element.classList.add('shake');
        setTimeout(() => {
            element.classList.remove('shake');
        }, 500);
    }
}
type FightResult = {
    isEnd: boolean,
    winner: Role,
    loser: Role,
}
function attack(attacker: Role, defender: Role) : FightResult {
    const {isCritical, damage} = calculateDamage(attacker.attack, defender.defense, attacker.critical_rate, attacker.critical_damage);
    $q.notify({
            message: `${attacker.name}攻击了${defender.name}，造成了${damage.toFixed(2)}点伤害${isCritical ? '，暴击了' : ''}`,
            color: 'primary',
          });
    if (isCritical && defender.card) {
        shake(defender.card);
    }
    defender.current_health -= damage;
    if (defender.current_health <= 0) {
        defender.current_health = 0;
        return {
            isEnd: true,
            winner: attacker,
            loser: defender,
        }
    }
    return {
        isEnd: false,
        winner: {} as Role,
        loser: {} as Role,
    }
}
async function fight(attacker: Role, defender: Role) {
    while (true) {
        const result = attack(attacker, defender);
        if (result.isEnd) {
            return result;
        }
        [attacker, defender] = [defender, attacker];
        // 停顿2s
        await new Promise((resolve) => {

            setTimeout(resolve, 2000);
        })
    }
}
async function decorate_fight() {
    const result = await api.get('game/get_fight_couple/');
    roles.value = result.data;
    roles.value.forEach((role: Role) => {
        role.current_health = role.health;
    })
    roles.value[0].current_health = roles.value[0].health;
    roles.value[1].current_health = roles.value[1].health;
    await fight(roles.value[0], roles.value[1]);
    $q.notify({
        message: `${result.data[0].name}战胜了${result.data[1].name}`,
        color: 'positive',
    })
}
</script>

<template>
  <q-dialog v-model="equipmentDetailConfig.showEquipmentDetail" persistent>
    <EquipmentDetail :equipment="equipmentDetailConfig.equipment" :close="equipmentDetailConfig.close" />
  </q-dialog>
  <q-page class="flex flex-center">
    <q-card class="q-ma-md" style="width: 400px" v-for="role in roles" :key="role.id" :ref="(el) => role.card = el ? el.$el : null">
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>{{role.name}}</q-item-label>
          </q-item-section>
        </q-item>
      </q-card-section>
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>生命值</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{role.current_health.toFixed(2)}} / {{role.health.toFixed(2)}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-linear-progress :value="role.current_health / role.health " />
      </q-card-section>
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>攻击力</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{role.attack.toFixed(2)}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item>
          <q-item-section>
            <q-item-label>防御力</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{role.defense.toFixed(2)}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item>
          <q-item-section>
            <q-item-label>暴击率</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{role.critical_rate.toFixed(2)}}%</q-item-label>
          </q-item-section>
        </q-item>
        <q-item>
          <q-item-section>
            <q-item-label>暴击伤害</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{role.critical_damage.toFixed(2)}}%</q-item-label>
          </q-item-section>
        </q-item>
      </q-card-section>
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>装备</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label v-for="equipment in role.equipments" :key="equipment.id" >
              <q-btn dense flat :label="equipment.name" :class="equipmentLevels[equipment.level - 1].color_class" @click="equipmentDetailConfig.open(equipment)" />
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-card-section>
    </q-card>


  </q-page>
</template>


<style scoped>

.shake {
  animation: shake 0.5s;
  animation-iteration-count: infinite;
}

@keyframes shake {
  0% { transform: translate(1px, 1px) rotate(0deg); }
  10% { transform: translate(-1px, -2px) rotate(-1deg); }
  20% { transform: translate(-3px, 0px) rotate(1deg); }
  30% { transform: translate(3px, 2px) rotate(0deg); }
  40% { transform: translate(1px, -1px) rotate(1deg); }
  50% { transform: translate(-1px, 2px) rotate(-1deg); }
  60% { transform: translate(-3px, 1px) rotate(0deg); }
  70% { transform: translate(3px, 1px) rotate(-1deg); }
  80% { transform: translate(-1px, -1px) rotate(1deg); }
  90% { transform: translate(1px, 2px) rotate(0deg); }
  100% { transform: translate(1px, -2px) rotate(-1deg); }
}
</style>
