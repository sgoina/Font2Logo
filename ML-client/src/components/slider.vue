<template>
  <div>
    <v-row justify="start" style="margin-bottom: 10px">
      <v-col cols="auto">
        <v-btn variant="outlined" @click="fetchAndSetAttributes" color="cyan"
          >Refresh Attributes</v-btn
        ></v-col
      >

      <v-col cols="auto"
        ><v-btn variant="outlined" @click="handleSliderInput" color="cyan"
          >Submit</v-btn
        ></v-col
      >
    </v-row>

    <v-slider
      v-for="(slider, index) in computedSlider"
      :key="index"
      v-model="initialValues[index]"
      :color="allcolor(index)"
      :label="slider.label"
      thumb-label
      thumb-size="30"
      :min="0"
      :max="100"
      :step="1"
      class="v-slider__track"
    ></v-slider>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed, watch } from "vue";
const initialValues = ref<number[]>([]);
const attr = ref("");
const emit = defineEmits(["input"]);
const props = defineProps({
  attrb: {
    type: String,
    required: true,
  },
  wordInput: {
    type: String,
    required: true,
  },
});
async function fetchAndSetAttributes() {
  attr.value = await fetch_attr(props.attrb);
  let jsonString = JSON.stringify(attr.value);
  let parsedData = JSON.parse(jsonString);
  let attributesArray = parsedData.data.map((item: any) => item.attributes);
  initialValues.value = Object.values(attributesArray[0]);
}
watch(
  () => props.attrb,
  (newValue, oldValue) => {
    if (newValue !== oldValue) {
      fetchAndSetAttributes();
    }
  }
);

async function fetch_attr(filename: string = "") {
  const response = await fetch(
    `http://127.0.0.1:5000/api/attributes/${filename}`,
    {
      method: "GET",
    }
  );
  return response.json();
}
const labels = [
  "angular",
  "artistic",
  "attention-grabbing",
  "attractive",
  "bad",
  "boring",
  "calm",
  "capitals",
  "charming",
  "clumsy",
  "complex",
  "cursive",
  "delicate",
  "disorderly",
  "display",
  "dramatic",
  "formal",
  "fresh",
  "friendly",
  "gentle",
  "graceful",
  "happy",
  "italic",
  "legible",
  "modern",
  "monospace",
  "playful",
  "pretentious",
  "serif",
  "sharp",
  "sloppy",
  "soft",
  "strong",
  "technical",
  "thin",
  "warm",
  "wide",
];

const allcolor = (index: number) => {
  if (initialValues.value[index] < 20) return "cyan";
  if (initialValues.value[index] < 30) return "purple";
  if (initialValues.value[index] < 40) return "teal";
  if (initialValues.value[index] < 50) return "blue";
  if (initialValues.value[index] < 60) return "green";
  if (initialValues.value[index] < 70) return "yellow";
  if (initialValues.value[index] < 80) return "orange";
  return "red";
};
const computedSlider = computed(() => {
  return initialValues.value.map((value, index) => ({
    label: labels[index],
    value: value,
  }));
});
//handle slider input
function handleSliderInput() {
  if (!props.wordInput) {
    alert("Please input text");
  } else {
    const regularArray = Array.from(initialValues.value);
    emit("input", regularArray);
  }
}
</script>

<style>
.v-slider__track {
  height: 40px;
  width: 1000px;
  margin-left: 110px;
}
</style>
