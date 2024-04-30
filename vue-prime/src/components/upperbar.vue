<script setup lang="ts">
import { defineComponent } from 'vue'
import bar from './bar.vue'

defineComponent({
  components: {
    bar
  }
})
</script>
<template>
  <div class="card">
    <Toolbar style="border-radius: 3rem; padding: 1rem 1rem 1rem 1.5rem; width: 70%">
      <template #start>
        <bar />
      </template>
      <template #center> </template>
      <template #end> </template>
    </Toolbar>
  </div>
</template>
<style scoped>
.card {
  display: flex;
  justify-content: center;
}
</style>
