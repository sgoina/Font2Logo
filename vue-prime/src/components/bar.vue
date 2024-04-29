<template>
  <Toast />
  <div class="grid card flex justify-content-center">
    <Sidebar v-model:visible="visibleLeft" header="Font2Logo" position="left">
      <p>Font2Logo is interesting</p>
      <ProgressBar :value="submitProgress" style="margin-bottom: 10%" />
      <div class="output-panel" ref="scrollPanel">
        <pre>{{ output }}</pre>
      </div>
    </Sidebar>
    <Sidebar v-model:visible="visibleTop" position="top" class="h-10rem md:h-30rem lg:h-50rem">
      <FileUpload
        mode="advanced"
        name="texture[]"
        url="http://127.0.0.1:8000/api/upload"
        accept="image/*"
        :maxFileSize="1000000"
        @upload="onUpload"
        ><template #empty>
          <p>
            Drag and drop files to here to upload and please name your texture files to
            glyh-paint.png and glyh-sem.png .
          </p>
        </template></FileUpload
      >
    </Sidebar>
    <div class="col">
      <Button
        style="height: 40px; width: 40px; font-size: 3rem"
        icon="pi  pi-cog"
        @click="visibleLeft = true"
      />
    </div>
    <div class="col">
      <Button @click="handleSubmit" style="width: 130px; height: 40px" label="Create Logo" />
    </div>
    <div class="col">
      <Button
        icon="pi pi-plus"
        @click="visibleTop = true"
        style="width: 190px; height: 41px"
        label="Change Texture"
      />
    </div>
    <div class="col">
      <InputText v-model="word" placeholder="word" />
    </div>
    <div class="col">
      <Dropdown v-model="selectedFontA" :options="listOfFonts" placeholder="FontA" />
    </div>
    <div class="col">
      <Dropdown v-model="selectedFontB" :options="listOfFonts" placeholder="FontB" />
    </div>
    <div class="col">
      <ToggleButton @click="switchTheme" v-model="Theme" onLabel="Dark" offLabel="Light" />
    </div>
    <div class="col">
      <Button @click="test" label="test " />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted, nextTick } from 'vue'
import { usePrimeVue } from 'primevue/config'
import { storeToRefs } from 'pinia'
import { useNumbersStore } from '@/stores/attribute'
import { useSubmitStore } from '@/stores/useSubmitstore'
import { fetch_api_att2font, post_api_att2font, post_api_Logo } from '@/utils/api'
import { useToast } from 'primevue/usetoast'
const PrimeVue = usePrimeVue()
const visibleLeft = ref(false)
const visibleTop = ref(false)
const Theme = ref(true)
const currentTheme = ref('viva-dark')
const word = ref('')
const AttrName = ref('')
const listOfFonts = ref([])
const selectedFontA = ref('')
const selectedFontB = ref('')
const toast = useToast()
const submitProgress = ref(0)
const output = ref('')
const scrollPanel = ref<HTMLElement | null>(null)
let intervalId: number | undefined = undefined

//call the stored numbers from pinia
const numbersStore = useNumbersStore()
const { numbers } = storeToRefs(numbersStore)
const submitStore = useSubmitStore()
async function test() {
  await switchfont()
}
//outputfetching for logo generator
const fetchOutput = () => {
  // Clear previous output
  // output.value = ''

  // Start fetching output continuously
  intervalId = setInterval(() => {
    fetch('http://127.0.0.1:8000/api/output')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then((data) => {
        output.value += data.output
        nextTick(() => {
          const panel = scrollPanel.value
          if (panel) {
            panel.scrollTop = panel.scrollHeight
          }
        })
      })
      .catch((error) => {
        console.error('Error:', error)
        // Handle the error or display an error message
      })
  }, 500) // Fetch every 1 second (adjust as needed)
}
onUnmounted(() => {
  // Clear the interval when the component is unmounted
  clearInterval(intervalId)
})
//stop fetching
const stopFetching = () => {
  clearInterval(intervalId)
  intervalId = undefined
}
//init for bar
onMounted(aquireAttrName)
onMounted(aquireFontList)
//fetches for the current targeted font style that you can change the attribute with
async function aquireAttrName() {
  try {
    const res = await fetch_api_att2font('/image/B', false)
    AttrName.value = res.data
    // console.log(AttrName.value)
  } catch (error) {
    console.error('Error aquiring AttrName', error)
    throw error
  }
}
async function aquireFontList() {
  try {
    const res = await fetch_api_att2font('/list', false)
    if (res) {
      listOfFonts.value = res.data
      console.log('fetched list of fonts')
    }
  } catch (error) {
    console.error('Error fetching list of fonts')
  }
}
async function switchfont() {
  if (!selectedFontA.value || !selectedFontB.value) {
    toast.add({
      severity: 'error',
      summary: 'Error Message',
      detail: 'you need both fonts selected',
      life: 3000
    })
    throw new Error('You need both fonts selected')
  } else {
    await post_api_att2font('/image', {
      imageA: selectedFontA.value,
      imageB: selectedFontB.value
    })
  }
  //update name for Attr
  await aquireAttrName()
}
const handleSubmit = async () => {
  try {
    submitProgress.value = 0
    if (word.value == '') {
      toast.add({
        severity: 'error',
        summary: 'Error Message',
        detail: 'you need to add a word input',
        life: 3000
      })
      throw new Error('you need to add a word input')
    }
    // Change font
    try {
      await switchfont()
    } catch (error) {
      console.error('Error changing font:', error)
      throw error // Throw the error to stop further execution
    }
    output.value += 'Format correct \n'
    // Change texture
    // Add code for changing texture here

    // Update attribute
    submitProgress.value = 20
    try {
      await post_api_att2font(`/attributes/${AttrName.value}`, numbers.value)
    } catch (error) {
      console.error('Error updating attribute:', error)
      throw error // Throw the error to stop further execution
    }
    submitProgress.value = 40
    output.value += 'attribute updated  \n'
    output.value += 'creating Font  \n'
    // Create font
    // Add code for creating font here
    try {
      await fetch_api_att2font(`/`, false)
    } catch (error) {
      console.error('Error creating Font', error)
      throw error // Throw the error to stop further execution
    }
    output.value += 'Font created  \n'
    output.value += 'creating Logo  \n'

    submitProgress.value = 80
    fetchOutput()
    // Create logo
    // Add code for creating logo here
    try {
      await post_api_Logo(`/create`, word.value)
    } catch (error) {
      console.error('Error creating Logo', error)
      throw error // Throw the error to stop further execution
    }
    stopFetching()
    submitProgress.value = 100
    output.value += 'Finished \n'

    // console.log(res_update_attribute.message)

    // Update the isSubmitted state after the submit action finishes
    submitStore.setSubmitted(true)
  } catch (error) {
    stopFetching()
    console.error('Error in handleSubmit:', error)
    // Handle the general error or show an error message
    // You can also perform any necessary cleanup or error handling here
  }
}

//for theme switching
const switchTheme = () => {
  let nextTheme = 'viva-light'
  if (currentTheme.value === 'viva-light') {
    nextTheme = 'viva-dark'
    Theme.value = false
  } else if (currentTheme.value === 'viva-dark') {
    nextTheme = 'viva-light'
    Theme.value = true
  }
  PrimeVue.changeTheme(currentTheme.value, nextTheme, 'id-to-link', () => {})
  // console.log(currentTheme.value)
  // console.log(nextTheme)
  currentTheme.value = nextTheme
}
const onUpload = () => {
  toast.add({
    severity: 'success',
    summary: 'file uploaded',
    detail: 'success',
    life: 3000
  })
}
</script>
<style scoped>
.output-panel {
  height: 500px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
}
</style>
