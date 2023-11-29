<script lang="ts" setup>
import {QCard} from 'quasar';
import {api} from 'boot/axios';
import {Ref, ref} from 'vue';
import CharacterCard from 'components/CharacterCard.vue';

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
const characters: Ref<Character[]> = ref([]);

async function loadData() {
  const response = await api.get('/game/character/list');
  characters.value = response.data;
  selectedCharacter.value = characters.value[0].id;
}
const selectedCharacter: Ref<number> = ref(0);
</script>

<template>
  <q-page class="flex flex-center">
    <q-card class="q-ma-md">
      <q-card-actions align="center">
        <q-btn color="primary" label="刷新" @click="loadData"/>
      </q-card-actions>
      <q-card-section v-if="characters.length > 0">
        <q-carousel
        v-model="selectedCharacter"
        transition-prev="scale"
        transition-next="scale"
        swipeable
        animated
        navigation
        padding
        arrows
        infinite
        class="q-pa-md q-gutter-md full-height"
        control-color="primary"
        control-size="2em"
      >
        <q-carousel-slide :name="character.id" v-for="character in characters" :key="character.id">
          <CharacterCard :character="character" />
        </q-carousel-slide>
      </q-carousel>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<style scoped>

</style>
