<template>
  <v-card>
    <v-divider></v-divider>
    <v-form>
      <v-col>
        <v-switch inset label="深色模式" v-model="dark_toggle"></v-switch>
        <v-text-field
          v-model="wordInput"
          label="Text"
          hint="No spaces"
          density="compact"
          variant="outlined"
          style="max-width: 200px; padding: 5px"
        ></v-text-field>

        <v-row style="margin: auto">
          <v-select
            style="max-width: 200px; padding: 5px"
            label="Result"
            variant="outlined"
            density="compact"
            :items="listOfFonts"
            v-model="imageB"
          ></v-select>

          <v-select
            style="max-width: 200px; padding: 5px"
            label="mimic"
            variant="outlined"
            density="compact"
            :items="listOfFonts"
            v-model="imageA"
          ></v-select>

          <v-divider></v-divider>
        </v-row>
      </v-col>
    </v-form>
    <v-form>
      <v-row>
        <v-col>
          <v-row style="margin: 2vh"
            ><v-btn @click="switchfont" variant="outlined" color="cyan"
              >Switch font</v-btn
            >
          </v-row>
          <v-row style="margin: 0.5vh">
            <v-col
              ><slider
                :wordInput="wordInput"
                :attrb="imageBattr"
                @input="handleUpdate"
              ></slider
            ></v-col>
            <v-col>
              <v-progress-linear
                v-model="progress"
                color="cyan"
                height="10"
                stream
                striped
              ></v-progress-linear>
              <v-divider
                style="margin-bottom: 20px; margin-top: 10px"
              ></v-divider>
              <v-col>
                <v-chip style="margin-bottom: 10px"> RESULT </v-chip>
                <v-row v-if="!loading"
                  ><v-col
                    v-for="(image, index) in images"
                    :key="index"
                    class="d-flex child-flex"
                    cols="4"
                  >
                    <v-img
                      :src="image"
                      aspect-ratio="1"
                      class="bg-grey-lighten-2"
                      draggable
                      max-height="250"
                      cover
                    >
                    </v-img> </v-col
                ></v-row>
                <v-row v-if="loading"
                  ><v-col
                    v-for="(image, index) in images"
                    :key="index"
                    class="d-flex child-flex"
                    cols="4"
                  >
                    <v-img
                      src="https://bad.src/not/valid"
                      aspect-ratio="1"
                      class="bg-grey-lighten-2"
                      lazy-src="src/assets/11-100x60.jpg"
                      max-height="250"
                    >
                      <template v-slot:placeholder>
                        <div
                          class="d-flex align-center justify-center fill-height"
                        >
                          <v-progress-circular
                            color="grey-lighten-4"
                            indeterminate
                          ></v-progress-circular>
                        </div>
                      </template>
                    </v-img>
                  </v-col>
                </v-row>
              </v-col>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-form>
  </v-card>
</template>
<script lang="ts" setup>
import { useTheme } from "vuetify/lib/framework.mjs";
import slider from "@/components/slider.vue";
import { watch, ref, onMounted } from "vue";
const listOfFonts = ref([]);
const imageB = ref();
const imageA = ref();
const imageBattr = ref("");
const wordInput = ref("");
const progress = ref(0);
const images = ref<string[]>([]);
const loading = ref(false);
const theme = useTheme();
const dark_toggle = ref(theme.global.name.value === "dark");
function apply_theme() {
  var theme_name = "";
  if (dark_toggle.value) {
    theme_name = "dark";
  } else {
    theme_name = "light";
  }
  theme.global.name.value = theme_name;
  localStorage.setItem("theme", theme_name);
}
apply_theme();
watch(dark_toggle, apply_theme);
async function change_attr(filename: string = "", data: object) {
  const response = await fetch(
    `http://127.0.0.1:5000/api/attributes/${filename}`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  );
  return response;
}
async function runLogo(input: string = "") {
  const response = await fetch(`http://127.0.0.1:8000/create`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(input),
  });
  return response;
}
async function fetch_api_logo(path: string = "") {
  const response = await fetch(`http://127.0.0.1:8000/results/${path}`, {
    method: "GET",
  });
  const blob = await response.blob();
  return URL.createObjectURL(blob);
}

async function fetch_api(path: string = "") {
  const response = await fetch(`http://127.0.0.1:5000/api/image/${path}`, {
    method: "GET",
  });
  const blob = await response.blob();
  return URL.createObjectURL(blob);
}
async function run_test() {
  const response = await fetch(`http://127.0.0.1:5000`, {
    method: "GET",
  });
  return response;
}
async function fetch_list() {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/list`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return null; // or handle the error appropriately
  }
}
async function fetch_imageB() {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/image/B `, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return null; // or handle the error appropriately
  }
}
async function fontlist() {
  try {
    const res = await fetch_list();
    if (res) {
      const data = res.data; // assuming your response structure has a 'data' field
      // Process your data here as needed
      listOfFonts.value = data;
      console.log(listOfFonts.value);
    } else {
      console.log("No data received");
    }
  } catch (error) {
    console.error("Error processing the font list:", error);
  }
}
//create a post for'/api/image'
async function give_image() {
  const response = await fetch(`http://127.0.0.1:5000/api/image`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      imageA: imageA.value,
      imageB: imageB.value,
    }),
  });
}

async function switchfont() {
  if (!imageA.value || !imageB.value) {
    alert("Please select both fonts");
  } else {
    await give_image();
    getimageB();
  }
}
async function getimageB() {
  // give_image();
  const res = await fetch_imageB();
  const data = res.data;
  imageBattr.value = data;
  console.log(imageBattr.value);
}
onMounted(getimageB);
onMounted(fontlist);
onMounted(getimages);
async function getimages() {
  for (let i = 0; i < 9; i++) {
    const res = await fetch_api_logo(`output00${i}.png`);
    images.value.push(res);
  }
  return true;
}
const handleUpdate = async (value: Array<GLfloat>) => {
  loading.value = true;
  progress.value = 0;

  const res = await change_attr(imageBattr.value, value);
  console.log(res);
  if (res.status !== 200) {
    loading.value = false;
    return; // Exit if the status is not 200
  }

  const res1 = await run_test();
  if (res1.status !== 200) {
    loading.value = false;
    return; // Exit if the status is not 200
  }
  progress.value = 25;

  const res2 = await runLogo(wordInput.value);
  if (res2.status !== 200) {
    loading.value = false;
    return; // Exit if the status is not 200
  }
  progress.value = 70;

  images.value = [];
  const res3 = await getimages();
  if (res3 !== true) {
    loading.value = false;
    return; // Exit if the status is not 200
  }
  progress.value = 100;

  loading.value = false;
};
</script>
<style>
.select {
  width: 200px;
}
</style>
