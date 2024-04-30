<template>
  <div style="width: 100%; height: 100%">
    <div>
      <template v-for="(_, index) in Math.ceil(Images.length / 9)" :key="index">
        <div style="width: 100%; box-sizing: border-box">
          <div style="display: flex; flex-wrap: nowrap; align-items: center">
            <template
              v-for="(item, logoIndex) in Images.slice(index * 9, (index + 1) * 9)"
              :key="`logo-${index}-${logoIndex}`"
            >
              <Image :src="item.itemImageSrc" :alt="item.alt" width="200" />
              <!-- <Divider
                v-if="logoIndex < Images.slice(index * 9, (index + 1) * 9).length - 1"
                layout="vertical"
                style="height: 200%; margin: 4px"
              /> -->
            </template>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'

interface Image {
  itemImageSrc: string
  alt: string
}

const props = defineProps({
  Images: {
    type: Array as () => Image[],
    required: true
  }
})

const { Images } = toRefs(props)
</script>
