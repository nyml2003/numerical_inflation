<script lang="ts" setup>
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
  birth: Date,
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
type Pause = {
  pause: boolean,
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
  {level: 5, color_class: 'text-red'},
  {level: 6, color_class: 'text-red-2'},
  {level: 7, color_class: 'text-red-3'},
  {level: 8, color_class: 'text-red-4'},
  {level: 9, color_class: 'text-pink'},
  {level: 10, color_class: 'text-yellow'},
]

const nullRole: Role = {
  id: 0,
  name: '角色',
  attack: 0,
  defense: 0,
  health: 0,
  current_health: 0,
  critical_rate: 0,
  critical_damage: 0,
  equipments: [],
  card: null,
  birth: new Date(),
}
const roles = ref<Role[]>([
  nullRole,
  nullRole,
])

function calculateDamage(attack: number, defense: number, critical_rate: number, critical_damage: number) {
  const random = Math.random() * 100;
  const isCritical: boolean = random < critical_rate;
  const critical_multiplier = isCritical ? 1 + critical_damage / 100 : 1;
  const reduction_multiplier = attack / (attack + defense);
  const random_multiplier = 1 + Math.random() * 0.2 - 0.1;
  const damage = attack * critical_multiplier * reduction_multiplier * random_multiplier;
  return {
    isCritical,
    damage,
  }
}

function shake(element: HTMLElement) {
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

async function attack(attacker: Role, defender: Role): Promise<FightResult> {
  const {
    isCritical,
    damage
  } = calculateDamage(attacker.attack, defender.defense, attacker.critical_rate, attacker.critical_damage);
  if (isCritical && defender.card) {
    shake(defender.card);
  }
  defender.current_health -= damage;
  if (!fastForwardInstance.value.fastForward) {
    log.value.push(`${attacker.name}对${defender.name}造成了${damage.toFixed(2)}点伤害`);
    await new Promise((resolve) => {
      setTimeout(() => {
        resolve(null);
      }, 2000);
    })
  }

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
    if (pauseInstance.value.pause) {
      await new Promise((resolve) => {
        setTimeout(() => {
          resolve(null);
        }, 1000);
      })
      continue;
    }

    const result = await attack(attacker, defender);
    if (result.isEnd) {
      return result;
    }
    [attacker, defender] = [defender, attacker];
  }
}

async function decorate_fight() {
  while (true) {
    await api.get('game/get_fight_couple/').then(async (result) => {
      roles.value = result.data;
      roles.value.forEach((role: Role) => {
        role.current_health = role.health;
      })
      roles.value[0].current_health = roles.value[0].health;
      roles.value[1].current_health = roles.value[1].health;
      if (fastForwardInstance.value.fastForward) {
        log.value.push(`${roles.value[0].name}与${roles.value[1].name}开始战斗`);
        await new Promise((resolve) => {
          setTimeout(() => {
            resolve(null);
          }, 2000);
        })
      }
      let res: FightResult;
      if (fastForwardInstance.value.fastForward) {
        const one2two_damage = calculateDamage(roles.value[0].attack, roles.value[1].defense, 100, roles.value[0].critical_damage);
        const two2one_damage = calculateDamage(roles.value[1].attack, roles.value[0].defense, 100, roles.value[1].critical_damage);
        if (one2two_damage.damage > two2one_damage.damage) {
          res = {
            isEnd: false,
            winner: roles.value[0],
            loser: roles.value[1],
          };
        } else {
          res = {
            isEnd: false,
            winner: roles.value[1],
            loser: roles.value[0],
          }
        }
      }else{
        res = await fight(roles.value[0], roles.value[1]);
      }
      roles.value = [nullRole, nullRole];
      const response = await api.post('game/handle_fight/', {
        winner: res.winner.id,
        loser: res.loser.id,
      })
      log.value.push(response.data.result);
    })
  }
}

const log = ref<string[]>([]);
onMounted(() => {
  decorate_fight();
})
const pauseInstance = ref<Pause>({
  pause: false,
})

function pause() {
  pauseInstance.value.pause = !pauseInstance.value.pause;
}

async function refresh() {
  pause();
  log.value = [];
  roles.value = [nullRole, nullRole];
  await api.get('game/init/');
  pause();
  await decorate_fight();
}

type health_status = {
  ratioInterval: number[],
  color: string,
}
const healthy: health_status = {
  ratioInterval: [0.8, 1],
  color: 'green',
}
const injured: health_status = {
  ratioInterval: [0.5, 0.8],
  color: 'orange',
}
const dying: health_status = {
  ratioInterval: [0, 0.5],
  color: 'red',
}
const dead: health_status = {
  ratioInterval: [-1, 0],
  color: 'black',
}
const health_status_list: health_status[] = [
  healthy,
  injured,
  dying,
  dead,
]

function getHealthStatus(current_health: number, health: number): health_status {
  const ratio = current_health / health;
  for (const health_status of health_status_list) {
    if (ratio >= health_status.ratioInterval[0] && ratio <= health_status.ratioInterval[1]) {
      return health_status;
    }
  }
  return dead;
}

//快进
type FastForward = {
  fastForward: boolean,
}
const fastForwardInstance = ref<FastForward>({
  fastForward: false,
})

function fastForward() {
  fastForwardInstance.value.fastForward = !fastForwardInstance.value.fastForward;
}

</script>

<template>
  <q-dialog v-model="equipmentDetailConfig.showEquipmentDetail" persistent>
    <EquipmentDetail :close="equipmentDetailConfig.close" :equipment="equipmentDetailConfig.equipment"/>
  </q-dialog>
  <q-page class="flex flex-center">
    <!--    刷新 暂停按钮 -->
    <q-btn-group>
      <q-btn color="green" label="刷新" @click="refresh()"/>
      <q-btn :color="pauseInstance.pause ? 'red' : 'green'" label="暂停" @click="pause()"/>
      <q-btn :color="fastForwardInstance.fastForward ? 'red' : 'green'" label="快进" @click="fastForward()"/>
    </q-btn-group>
    <q-card v-for="role in roles" :key="role.id" :ref="(el) => role.card = el ? el.$el : null" class="q-ma-md"
            style="width: 400px">
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>{{ role.name }}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{ role.birth.toLocaleString().replace('T', ' ') }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-card-section>
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>生命值</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{ role.current_health.toFixed(2) }} / {{ role.health.toFixed(2) }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-linear-progress :color="getHealthStatus(role.current_health, role.health).color"
                           :value="role.current_health / role.health "/>
      </q-card-section>
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>攻击力</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{ role.attack.toFixed(2) }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item>
          <q-item-section>
            <q-item-label>防御力</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{ role.defense.toFixed(2) }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item>
          <q-item-section>
            <q-item-label>暴击率</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{ role.critical_rate.toFixed(2) }}%</q-item-label>
          </q-item-section>
        </q-item>
        <q-item>
          <q-item-section>
            <q-item-label>暴击伤害</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>{{ role.critical_damage.toFixed(2) }}%</q-item-label>
          </q-item-section>
        </q-item>
      </q-card-section>
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>装备</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label v-for="equipment in role.equipments" :key="equipment.id">
              <q-btn :class="equipmentLevels[equipment.level - 1].color_class" :label="equipment.name" dense flat
                     @click="equipmentDetailConfig.open(equipment)"/>
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-card-section>
    </q-card>
    <q-card style="width: 1600px">
      <q-card-section>
        <q-item>
          <q-item-section>
            <q-item-label>战斗日志</q-item-label>
          </q-item-section>
        </q-item>
      </q-card-section>
      <q-card-section>
        <q-scroll-area style="height: 400px; height: 300px;">
          <q-list bordered>
            <q-item v-for="item in log" :key="item">
              <q-item-section>{{ item }}</q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
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
  0% {
    transform: translate(1px, 1px) rotate(0deg);
  }
  10% {
    transform: translate(-1px, -2px) rotate(-1deg);
  }
  20% {
    transform: translate(-3px, 0px) rotate(1deg);
  }
  30% {
    transform: translate(3px, 2px) rotate(0deg);
  }
  40% {
    transform: translate(1px, -1px) rotate(1deg);
  }
  50% {
    transform: translate(-1px, 2px) rotate(-1deg);
  }
  60% {
    transform: translate(-3px, 1px) rotate(0deg);
  }
  70% {
    transform: translate(3px, 1px) rotate(-1deg);
  }
  80% {
    transform: translate(-1px, -1px) rotate(1deg);
  }
  90% {
    transform: translate(1px, 2px) rotate(0deg);
  }
  100% {
    transform: translate(1px, -2px) rotate(-1deg);
  }
}
</style>
