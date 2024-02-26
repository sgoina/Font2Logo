<script setup lang="ts">
import { useToast } from "primevue/usetoast";
import Toast from "primevue/toast";
import Button from "primevue/button";

const toast = useToast();

const showSuccess = () => {
  toast.add({
    severity: "success",
    summary: "Success Message",
    detail: "Message Content",
    life: 3000,
  });
};

const showInfo = () => {
  toast.add({
    severity: "info",
    summary: "Info Message",
    detail: "Message Content",
    life: 3000,
  });
};

const showWarn = () => {
  toast.add({
    severity: "warn",
    summary: "Warn Message",
    detail: "Message Content",
    life: 3000,
  });
};

const showError = () => {
  toast.add({
    severity: "error",
    summary: "Error Message",
    detail: "Message Content",
    life: 3000,
  });
};

const showSecondary = () => {
  toast.add({
    severity: "secondary",
    summary: "Secondary Message",
    detail: "Message Content",
    life: 3000,
  });
};

const showContrast = () => {
  toast.add({
    severity: "contrast",
    summary: "Contrast Message",
    detail: "Message Content",
    life: 3000,
  });
};
</script>
<template>
  <Toast />
  <div class="flex flex-wrap gap-2">
    <Button
      label="Success"
      severity="success"
      @click="showSuccess"
      text
      raised
    />
    <Button label="Info" severity="info" @click="showInfo" text raised />
    <Button label="Warn" severity="warning" @click="showWarn" text raised />
    <Button label="Error" severity="danger" @click="showError" text raised />
    <Button
      label="Secondary"
      severity="secondary"
      @click="showSecondary"
      text
      raised
    />
    <Button
      label="Contrast"
      severity="contrast"
      @click="showContrast"
      text
      raised
    />
  </div>
</template>
