<template>
  <div class="card flex flex-column gap-3">
    <Timeline :value="events" layout="horizontal" align="top" style="width: 110vh">
      <template #content="slotProps">
        {{ slotProps.item }}
      </template>
    </Timeline>
    <div class="grid">
      <div class="col">1</div>
      <div class="col-4">2</div>
      <div class="col-4">3</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const events = ref(['FONT', 'LOGO', 'TEXTURE'])
</script>
