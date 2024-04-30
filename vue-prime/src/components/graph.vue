<template>
  <Card style="height: 70%; width: 100%">
    <template #content>
      <Chip v-if="imageA.itemImageSrc" label="Font A" />
      <Image :src="imageA.itemImageSrc" width="100%" />

      <Chip v-if="imageB.itemImageSrc" label="Font B" />
      <Image :src="imageB.itemImageSrc" width="100%" />

      <Chip v-if="attrImages.itemImageSrc" label="created Font" />
      <Image :src="attrImages.itemImageSrc" width="100%" />

      <Chip v-if="logoImages.length > 0" label="Logo Images" />
      <photo :Images="logoImages" />

      <Chip v-if="results.length > 0" label="Result Images" />
      <photo :Images="results" />
    </template>
  </Card>

  <!-- <Button @click="test" label="test"></Button> -->
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useSubmitStoreFont, useSubmitStore, useFontStore } from '@/stores/useSubmitstore'
import { fetch_api_att2font, fetch_api_Logo, post_api_att2font } from '@/utils/api'
import photo from '@/components/photo.vue'
import Chip from 'primevue/chip'

const submitStore = useSubmitStore()
const { isSubmitted } = storeToRefs(submitStore)
const submitStoreFont = useSubmitStoreFont()
const { isSubmittedFont } = storeToRefs(submitStoreFont)
const fontStore = useFontStore()
const { fontChanged, a, b } = storeToRefs(fontStore)

const attrImages = ref<{ itemImageSrc: string; alt: string }>({ itemImageSrc: '', alt: '' })
const imageA = ref<{ itemImageSrc: string; alt: string }>({ itemImageSrc: '', alt: '' })
const imageB = ref<{ itemImageSrc: string; alt: string }>({ itemImageSrc: '', alt: '' })
const logoImages = ref<{ itemImageSrc: string; alt: string }[]>([])
const results = ref<{ itemImageSrc: string; alt: string }[]>([])
async function fetchFont() {
  attrImages.value = { itemImageSrc: '', alt: '' }
  const attr = await fetch_api_att2font(`/attr/all_characters.png`, true)
  attrImages.value = { itemImageSrc: attr, alt: `Generated Image full` }
}
async function fetchPicture() {
  logoImages.value = []
  results.value = []

  for (let i = 0; i < 9; i++) {
    const res = await fetch_api_Logo(`/results/output00${i}.png`, true)
    results.value.push({ itemImageSrc: res, alt: `Generated Image ${i}` })

    const logo = await fetch_api_Logo(`/logo/00${i}.png`, true)
    logoImages.value.push({ itemImageSrc: logo, alt: `Generated Image ${i}` })
  }
}

function test() {
  fetchPicture()
}

watch(isSubmitted, (value) => {
  if (value) {
    fetchPicture()
    submitStore.setSubmitted(false)
  }
})
watch(isSubmittedFont, (value) => {
  if (value) {
    fetchFont()
    submitStoreFont.setSubmitted(false)
  }
})
watch(fontChanged, async (value) => {
  if (value) {
    if (a.value == true && b.value == false) {
      await post_api_att2font(`/saveattr`, { switch: 'a' })
    } else if (b.value == true && a.value == false) {
      await post_api_att2font(`/saveattr`, { switch: 'b' })
    } else if (b.value == true && a.value == true) {
      await post_api_att2font(`/saveattr`, { switch: 'a' })
      await post_api_att2font(`/saveattr`, { switch: 'b' })
    }

    if (a.value == true && b.value == false) {
      const imgA = await fetch_api_att2font(`/attr/all_characters_a.png`, true)
      imageA.value = { itemImageSrc: imgA, alt: `Generated Image full` }
    } else if (b.value == true && a.value == false) {
      const imgB = await fetch_api_att2font(`/attr/all_characters_b.png`, true)
      imageB.value = { itemImageSrc: imgB, alt: `Generated Image full` }
    } else if (b.value == true && a.value == true) {
      const imgA = await fetch_api_att2font(`/attr/all_characters_a.png`, true)
      const imgB = await fetch_api_att2font(`/attr/all_characters_b.png`, true)
      imageA.value = { itemImageSrc: imgA, alt: `Generated Image full` }
      imageB.value = { itemImageSrc: imgB, alt: `Generated Image full` }
    }

    fontStore.setChanged(false)
  }
})
</script>
