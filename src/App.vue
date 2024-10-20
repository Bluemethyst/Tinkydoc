<script lang="ts">
import { defineComponent, ref, provide } from "vue";
import { RouterLink, RouterView } from "vue-router";

export default defineComponent({
    name: "App",
    setup() {
        const lang = ref("en_us"); // default language
        provide("lang", lang); // provide the language state
        return {
            lang,
        };
    },
});
</script>

<template>
    <RouterView />
</template>
