<script setup lang="ts">
import { ref } from 'vue'
import attributeSlider from '@/components/attributeSlider.vue'
import graph from '@/components/graph.vue'

const numbers = ref<number[]>([])
const handleNumbers = (newNumbers: number[]) => {
  numbers.value = newNumbers
}
</script>

<template>
  <div class="grid">
    <div class="col">
      <attributeSlider @update:numbers="handleNumbers" />
    </div>
    <div class="col-10">
      <h2>Font2Logo</h2>
      <graph />
    </div>
  </div>
</template>
