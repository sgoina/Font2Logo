<template>
  <div style="width: 100%; height: 100vh">
    <ScrollPanel style="width: 100%; height: 100%">
      <div style="display: flex; flex-direction: column">
        <div
          v-for="(item, index) in images"
          :key="index"
          style="flex: 0 0 auto; width: 100%; padding: 2px; box-sizing: border-box"
        >
          <ScrollPanel style="width: 100%; height: 80vh">
            <div style="display: flex; flex-wrap: nowrap; overflow-x: auto">
              <img
                :src="item.itemImageSrc"
                :alt="item.alt"
                style="width: auto; height: 100%; object-fit: contain"
              />
            </div>
          </ScrollPanel>
        </div>
      </div>
    </ScrollPanel>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Image {
  itemImageSrc: string
  alt: string
}

const props = defineProps({
  images: {
    type: Array as () => Image[],
    required: true
  }
})

const images = ref(props.images)
</script>
