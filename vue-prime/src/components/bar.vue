<template>
  <Toast />
  <div class="grid card flex justify-content-center">
    <Sidebar v-model:visible="visible" header="Font2Logo">
      <p>Font2Logo is interesting</p>
      <ProgressBar :value="50" />
    </Sidebar>
    <div class="col">
      <Button
        style="height: 40px; width: 40px; font-size: 3rem"
        icon="pi  pi-cog"
        @click="visible = true"
      />
    </div>
    <div class="col">
      <Button @click="handleSubmit" style="width: 130px; height: 40px" label="Create Logo" />
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
    <!-- <div class="col">
      <FileUpload
        mode="basic"
        name="paint"
        url="/api/upload"
        accept="image/*"
        :maxFileSize="1000000"
        @upload="onUpload"
      />
    </div>
    <div class="col">
      <FileUpload
        mode="basic"
        name="sem"
        url="/api/upload"
        accept="image/*"
        :maxFileSize="1000000"
        @upload="onUpload"
      />
    </div> -->
    <div class="col">
      <!-- <Button @click="test"> test</Button> -->
    </div>
    <div class="col">
      <ToggleButton @click="switchTheme" v-model="Theme" onLabel="Dark" offLabel="Light" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { usePrimeVue } from 'primevue/config'
import { storeToRefs } from 'pinia'
import { useNumbersStore } from '@/stores/attribute'
import { useSubmitStore } from '@/stores/useSubmitstore'
import { fetch_api_att2font, post_api_att2font, post_api_Logo } from '@/utils/api'
import { useToast } from 'primevue/usetoast'
const PrimeVue = usePrimeVue()
const visible = ref(false)
const Theme = ref(true)
const currentTheme = ref('viva-dark')
const word = ref('')
const AttrName = ref('')
const listOfFonts = ref([])
const selectedFontA = ref('')
const selectedFontB = ref('')
const toast = useToast()

//call the stored numbers from pinia
const numbersStore = useNumbersStore()
const { numbers } = storeToRefs(numbersStore)
const submitStore = useSubmitStore()

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
async function test() {
  if (word.value == '') console.log('hello')
}
const handleSubmit = async () => {
  try {
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

    // Change texture
    // Add code for changing texture here

    // Update attribute
    try {
      await post_api_att2font(`/attributes/${AttrName.value}`, numbers.value)
    } catch (error) {
      console.error('Error updating attribute:', error)
      throw error // Throw the error to stop further execution
    }

    // Create font
    // Add code for creating font here
    try {
      await fetch_api_att2font(`/`, false)
    } catch (error) {
      console.error('Error creating Font', error)
      throw error // Throw the error to stop further execution
    }

    // Create logo
    // Add code for creating logo here
    try {
      await post_api_Logo(`/create`, word.value)
    } catch (error) {
      console.error('Error creating Logo', error)
      throw error // Throw the error to stop further execution
    }

    // console.log(res_update_attribute.message)

    // Update the isSubmitted state after the submit action finishes
    submitStore.setSubmitted(true)
  } catch (error) {
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
const onUpload = () => {}
</script>
