<template>
  <div style="width: 100%; height: 100%">
    <ScrollPanel
      position="bottom"
      :pt="{
        wrapper: {
          style: { 'border-right': '10px solid var(--surface-ground)' }
        }
      }"
    >
      <div>
        <template
          v-for="(_, index) in Math.max(attrImages.length, Math.ceil(logoImages.length / 9))"
          :key="index"
        >
          <div v-if="index < attrImages.length" style="width: 100%; box-sizing: border-box">
            <img
              :src="attrImages[index].itemImageSrc"
              :alt="attrImages[index].alt"
              style="width: 100%; height: auto; object-fit: cover"
            />
          </div>
          <div
            v-if="index < Math.ceil(logoImages.length / 9)"
            style="width: 100%; box-sizing: border-box"
          >
            <div style="display: flex; flex-wrap: nowrap; align-items: center">
              <template
                v-for="(item, logoIndex) in logoImages.slice(index * 9, (index + 1) * 9)"
                :key="`logo-${index}-${logoIndex}`"
              >
                <Image :src="item.itemImageSrc" :alt="item.alt" width="200" />
                <Divider
                  v-if="logoIndex < logoImages.slice(index * 9, (index + 1) * 9).length - 1"
                  layout="vertical"
                  style="height: 200%; margin: 4px"
                />
              </template>
            </div>
          </div>
        </template>
      </div>
    </ScrollPanel>
  </div>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'
import ScrollPanel from 'primevue/scrollpanel'
import Divider from 'primevue/divider'

interface Image {
  itemImageSrc: string
  alt: string
}

const props = defineProps({
  attrImages: {
    type: Array as () => Image[],
    required: true
  },
  logoImages: {
    type: Array as () => Image[],
    required: true
  }
})

const { attrImages, logoImages } = toRefs(props)
</script>
