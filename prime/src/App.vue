<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import TabView from "primevue/tabview";
import TabPanel from "primevue/tabpanel";
import Sidebar from "primevue/sidebar";
import { ref } from "vue";
import Button from "primevue/button";
import { usePrimeVue } from "primevue/config";
import Image from "primevue/image";
import callout from "@/components/callout.vue";
import "primeicons/primeicons.css";
import Chip from "primevue/chip";
import Message from "primevue/message";
const visible = ref(false);
const PrimeVue = usePrimeVue();

const selectNoirTheme = () => {
  // 1. Current theme name
  // 2. Next theme name
  // 3. id of <link>, what reference to where set theme css file
  PrimeVue.changeTheme(
    "aura-dark-green",
    "aura-dark-noir",
    "id-to-link",
    () => {}
  );
};

// if current theme is light
const selectGreenTheme = () => {
  // 1. Current theme name
  // 2. Next theme name
  // 3. id of <link>, what reference to where set theme css file
  PrimeVue.changeTheme(
    "aura-dark-noir",
    "aura-dark-green",
    "id-to-link",
    () => {}
  );
};
</script>

<template>
  <div class="card flex justify-content-center">
    <Sidebar v-model:visible="visible" header="Options">
      <TabView>
        <TabPanel header="Router">
          <RouterLink to="/"><Button label="Home" text raised /></RouterLink>
        </TabPanel>
        <TabPanel header="Colors">
          <Button
            label="Green Theme"
            @click="selectGreenTheme"
            outlined
            rounded
            class="butt"
          ></Button>
          <Button
            label="Noir Theme"
            @click="selectNoirTheme"
            rounded
            outlined
            class="butt"
          ></Button>
        </TabPanel>
        <TabPanel header="testing stuff">
          <div
            v-ripple="{
              pt: {
                root: { style: 'background: rgba(75, 175, 80, 0.3)' },
              },
            }"
            class="box p-ripple bg-primary flex select-none justify-content-center align-items-center border-round p-6 font-bold"
            style="border: 1px solid rgba(75, 175, 80, 0.3)"
          >
            Default
          </div>
          <callout />
        </TabPanel>
      </TabView>
    </Sidebar>
  </div>
  <div class="card flex justify-content-start">
    <Button
      severity="secondary"
      @click="visible = true"
      outlined
      class="border-round"
      ><Image class="butt" src="./hutao.png" alt="Image" width="50px"></Image
      ><Message severity="error" icon="pi pi-spin pi-cog" :closable="false"
        >The menu</Message
      ></Button
    >
  </div>

  <RouterView />
</template>
<style>
.butt {
  margin: 10px;
}
.tab {
  width: 1000px;
  height: 100px;
}
.box {
  background: var(--surface-card);
  padding: 2rem;
  border-radius: 10px;
  width: 110px;
  text-align: center;
}
</style>
