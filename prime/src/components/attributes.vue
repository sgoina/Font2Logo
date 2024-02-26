<template>
  <div class="container">
    <Card>
      <template #title>Attributes</template>
      <template #content>
        <Knob class="big-knob" v-model="value" :min="0" :max="100" :step="1" />
        <Knob class="big-knob" v-model="value" :min="0" :max="100" :step="1" />
        <Knob class="big-knob" v-model="value" :min="0" :max="100" :step="1" />
      </template>
    </Card>
  </div>
</template>
<script setup lang="ts">
import Card from "primevue/card";
import Knob from "primevue/knob";
import { ref } from "vue";
import Button from "primevue/button";
const value = ref(0);
</script>
<style>
.container {
  display: flex;
  align-items: center;
  height: 50vh;
}
.big-knob {
  width: 100px;
  height: 100px;
}
</style>
