<script lang="ts" setup>
import {onMounted} from "vue";

onMounted(()=>{
 //按钮每1s闪烁一次
  setInterval(()=>{
    if (document.querySelector('button')) {
      shake(document.querySelector('button') as HTMLElement);
    }
  },1000)
})
function shake(element: HTMLElement) {
  if (element instanceof HTMLElement) {
    element.classList.add('shake');
    setTimeout(() => {
      element.classList.remove('shake');
    }, 500);
  }
}
</script>
<template>
  <button>
    mouseover me and I will shake
  </button>
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
