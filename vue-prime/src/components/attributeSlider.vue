<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import Slider from 'primevue/slider'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'
import { useNumbersStore } from '@/stores/attribute'

const numbersStore = useNumbersStore()

interface Attribute {
  attr: string
  num: number
}

const array = ref<Attribute[]>([])

const labels = [
  'angular',
  'artistic',
  'attention-grabbing',
  'attractive',
  'bad',
  'boring',
  'calm',
  'capitals',
  'charming',
  'clumsy',
  'complex',
  'cursive',
  'delicate',
  'disorderly',
  'display',
  'dramatic',
  'formal',
  'fresh',
  'friendly',
  'gentle',
  'graceful',
  'happy',
  'italic',
  'legible',
  'modern',
  'monospace',
  'playful',
  'pretentious',
  'serif',
  'sharp',
  'sloppy',
  'soft',
  'strong',
  'technical',
  'thin',
  'warm',
  'wide'
]

onMounted(() => {
  array.value = labels.map((label, index) => ({
    attr: label,
    num: numbersStore.numbers[index] || 0
  }))
})

const assignRandomNumbers = () => {
  numbersStore.updateNumbers(labels.map(() => Math.floor(Math.random() * 101)))
}

watch(
  () => numbersStore.numbers,
  (newNumbers) => {
    array.value = labels.map((label, index) => ({
      attr: label,
      num: newNumbers[index] || 0
    }))
  },
  { deep: true }
)
</script>

<template>
  <ScrollPanel
    style="width: 250px; height: 85vh; margin: 2%"
    :pt="{
      wrapper: {
        style: { 'border-right': '10px solid var(--surface-ground)' }
      },
      bary: 'hover:bg-primary-400 bg-primary-300 opacity-100'
    }"
  >
    <h2 style="margin-left: 2%; margin-bottom: 3%">Attributes</h2>
    <h2>
      <Button
        style="margin-left: 1.5%"
        label="Assign Random Numbers"
        @click="assignRandomNumbers"
      />
    </h2>
    <div v-for="(attr, index) in array" :key="index">
      <p style="margin-left: 5%; margin-right: 3%">{{ attr.attr }}: {{ attr.num }}</p>
      <Slider
        v-model="numbersStore.numbers[index]"
        class="w-14rem"
        style="margin-left: 5%; margin-right: 3%; margin-bottom: 3%"
      />
    </div>
  </ScrollPanel>
</template>
