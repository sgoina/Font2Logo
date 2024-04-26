<template>
  <div style="width: 30vh; height: 70vh">
    <Galleria
      :value="images"
      :numVisible="3"
      containerStyle="max-width: 640px"
      :showThumbnails="false"
      :showIndicators="true"
      :changeItemOnIndicatorHover="true"
      :showIndicatorsOnItem="true"
      indicatorsPosition="left"
    >
      <template #item="{ item }">
        <img :src="item.itemImageSrc" :alt="item.alt" style="width: 100%; display: block" />
      </template>
      <template #indicator="{ index }">
        <span style="color: '#ffffff'">{{ index + 1 }}</span>
      </template>
    </Galleria>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    required: true
  }
})

const images = ref(props.images)
</script>
