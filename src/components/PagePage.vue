<script lang="ts">
import { defineComponent, watch, ref, inject } from "vue";
import { useRouter } from "vue-router";
import LangSelect from "./LangSelect.vue";
import type { ResponseType } from "@/types";
import { textSpanContainsPosition } from "typescript";

export default defineComponent({
    name: "PagePage",
    setup() {
        const responseData = ref<string | ResponseType>();
        const router = useRouter();
        const lang = inject("lang");

        const selectedLanguage = ref("en_us");

        const fetchData = async (pathMatch: string | string[]) => {
            if (Array.isArray(pathMatch)) {
                pathMatch = pathMatch.join("/");
            }

            // Split the pathMatch by backslashes
            let parts = pathMatch.split("/");
            console.log(parts);
            let index;
            // Find the index of "encyclopedia"
            if (pathMatch.includes("encyclopedia")) {
                index = parts.indexOf("encyclopedia");
                console.log(index);
            } else if (pathMatch.includes("mighty_smelting")) {
                index = parts.indexOf("mighty_smelting");
                console.log(index);
            } else if (pathMatch.includes("fantastic_foundry")) {
                index = parts.indexOf("fantastic_foundry");
                console.log(index);
            } else if (pathMatch.includes("materials_and_you")) {
                index = parts.indexOf("materials_and_you");
                console.log(index);
            } else if (pathMatch.includes("puny_smelting")) {
                index = parts.indexOf("puny_smelting");
                console.log(index);
            } else if (pathMatch.includes("tinkers_gadgetry")) {
                index = parts.indexOf("tinkers_gadgetry");
                console.log(index);
            } else {
                index = -1;
            }

            // Insert the desired string after "encyclopedia"
            if (index !== -1) {
                parts.splice(index + 1, 0, selectedLanguage.value);
            }

            console.log(pathMatch);
            // Join the parts back into a string
            pathMatch = parts.join("/");
            console.log(pathMatch);

            try {
                const response = await fetch(`/book/${pathMatch}.json`);
                const contentType = response.headers.get("content-type");

                if (
                    !response.ok ||
                    (contentType && contentType.includes("text/html"))
                ) {
                    responseData.value = "File not found";
                } else if (contentType && contentType.includes("image/png")) {
                    responseData.value = "Image not loading";
                } else {
                    responseData.value = await response.json();
                }
            } catch (error) {
                console.error(error);
                responseData.value = "An error occurred";
            }
        };

        watch(
            () => router.currentRoute.value,
            (route) => {
                console.log(route);
                fetchData(route.params.pathMatch);
            }
        );

        // Fetch data initially when the component is mounted
        fetchData(router.currentRoute.value.params.pathMatch);

        return {
            responseData,
            lang,
        };
    },
});
</script>

<template>
    <p v-if="!responseData">Fetching data...</p>
    <div v-else-if="typeof responseData !== 'string'">
        <h1>{{ responseData.title }}</h1>
        <p v-for="text in responseData.text">{{ text.text }}</p>
    </div>
    <div v-else>
        <p>{{ responseData }}</p>
    </div>
</template>
