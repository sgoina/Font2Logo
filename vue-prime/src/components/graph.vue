<template>
  <Card style="height: 70%; width: 100%">
    <template #content>
      <photot :attrImages="attrImages" :logoImages="logoImages" />
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useSubmitStore } from '@/stores/useSubmitstore'
import { fetch_api_att2font, fetch_api_Logo } from '@/utils/api'
// import photo from '@/components/photo.vue'
import photot from '@/components/photot.vue'

const submitStore = useSubmitStore()
const { isSubmitted } = storeToRefs(submitStore)

// const results = ref<{ itemImageSrc: string; alt: string }[]>([])
const logoImages = ref<{ itemImageSrc: string; alt: string }[]>([])
const attrImages = ref<{ itemImageSrc: string; alt: string }[]>([])

async function fetchPicture() {
  logoImages.value = []
  attrImages.value = []

  for (let i = 0; i < 9; i++) {
    // const res = await fetch_api_Logo(`/results/output00${i}.png`, true)
    // results.value.push({ itemImageSrc: res, alt: `Generated Image ${i}` })
    const logo = await fetch_api_Logo(`/logo/00${i}.png`, true)
    logoImages.value.push({ itemImageSrc: logo, alt: `Generated Image ${i}` })
  }
  for (let i = 0; i < 9; i++) {
    const res = await fetch_api_Logo(`/results/output00${i}.png`, true)
    logoImages.value.push({ itemImageSrc: res, alt: `Generated Image ${i}` })
    // const logo = await fetch_api_Logo(`/logo/00${i}.png`, true)
    // logoImages.value.push({ itemImageSrc: logo, alt: `Generated Image ${i}` })
  }
  console.log(logoImages.value)
  const attr = await fetch_api_att2font(`/attr/all_characters.png`, true)
  attrImages.value.push({ itemImageSrc: attr, alt: `Generated Image full` })
}

watch(isSubmitted, (value) => {
  if (value) {
    fetchPicture()
    submitStore.setSubmitted(false)
  }
})
</script>
