<template>
  <div class="card">
    <Splitter style="height: 75vh; margin-right: 10vh" class="mb-5">
      <SplitterPanel class="flex align-items-center justify-content-center"
        ><photo :images="attrImages"
      /></SplitterPanel>
      <SplitterPanel class="flex align-items-center justify-content-center">
        <photo :images="logoImages"
      /></SplitterPanel>
      <SplitterPanel class="flex align-items-center justify-content-center">
        <div>
          <photo :images="results" />
        </div>
      </SplitterPanel>
    </Splitter>
  </div>
  <!-- <Button @click="fetchPicture">get image</Button> -->
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useSubmitStore } from '@/stores/useSubmitstore'
import { fetch_api_att2font, fetch_api_Logo } from '@/utils/api'
import photo from '@/components/photo.vue'
const submitStore = useSubmitStore()
const { isSubmitted } = storeToRefs(submitStore)
const results = ref<{ itemImageSrc: string; alt: string }[]>([])
const logoImages = ref<{ itemImageSrc: string; alt: string }[]>([])
const attrImages = ref<{ itemImageSrc: string; alt: string }[]>([])

async function fetchPicture() {
  // Fetch the picture from the server

  for (let i = 0; i < 9; i++) {
    const res = await fetch_api_Logo(`/results/output00${i}.png`, true)
    results.value.push({ itemImageSrc: res, alt: `Generated Image ${i}` })

    const logo = await fetch_api_Logo(`/logo/00${i}.png`, true)
    logoImages.value.push({ itemImageSrc: logo, alt: `Generated Image ${i}` })
  }
  const attr = await fetch_api_att2font(`/attr/all_characters.png`, true)
  attrImages.value.push({ itemImageSrc: attr, alt: `Generated Image full` })
  // console.log(images)
  // const res = await fetch_api_Logo(`/results/output000.png`, true)

  // const response = await fetch('path/to/picture')
  // picture.value = await response.blob()
}
watch(isSubmitted, (value) => {
  if (value) {
    fetchPicture()
    submitStore.setSubmitted(false) // Reset the isSubmitted state
  }
})
</script>
