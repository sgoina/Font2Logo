<script>
// useSliders.js
import { reactive } from "vue";

export function useSliders(initialValues) {
  const sliders = reactive(
    initialValues.map((value, index) => ({
      label: [
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
      ][index],
      value: value,
      color: [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
        "red",
        "orange",
      ][index],
    }))
  );

  function updateSlider(index, newValue) {
    sliders[index].value = newValue;
  }

  return {
    sliders,
    updateSlider,
  };
}
</script>
