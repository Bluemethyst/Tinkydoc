<script lang="ts">
import { defineComponent, watchEffect, ref, watch, reactive } from "vue";
import LangSelect from "./LangSelect.vue";
import NavBar from "./NavBar.vue";
import { useRouter } from "vue-router";

export default defineComponent({
    name: "HomePage",
    components: {
        NavBar,
    },
    setup() {
        const router = useRouter();
        const searchQuery = ref("");
        watch(
            () => router.currentRoute.value.query,
            (newQuery: any) => {
                if (newQuery.searchQuery) {
                    searchQuery.value = newQuery.searchQuery as string;
                }
            },
            { immediate: true }
        );
        watchEffect(() => {
            if (searchQuery.value !== "") {
                router.push({ path: "/", query: { q: searchQuery.value } });
            } else {
                router.push({ path: "/" });
            }
        });
        return {
            responseData: "",
            searchQuery,
            fileList: [] as string[],
            filteredFiles: [] as string[],
        };
    },
    mounted() {
        fetch("/kept_files.json")
            .then((response) => response.json())
            .then((data) => {
                this.fileList = data.files;
            });
        if (this.$route.query.q) {
            this.searchQuery = this.$route.query.q as string;
            this.searchFiles();
            this.$forceUpdate();
        }
    },

    methods: {
        removeDuplicate(arr: any[]): string[] {
            return Array.from(new Set(arr));
        },
        removePart(str: string, i: any) {
            this.filteredFiles[i] = this.filteredFiles[i].replace(str, "");
        },
        searchFiles() {
            console.log(this.searchQuery);
            this.filteredFiles = this.fileList.filter((file) =>
                file.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
            const langs = [
                "en_us\\",
                "ja_jp\\",
                "ko_kr\\",
                "pt_br\\",
                "ru_ru\\",
                "tr_tr\\",
                "zh_cn\\",
                "zh_tw\\",
            ];
            for (let i in this.filteredFiles) {
                this.removePart(".json", i);
                this.removePart("book", i);
                for (let lang of langs) {
                    if (this.filteredFiles[i].includes(lang)) {
                        this.removePart(lang, i);
                    }
                }
            }
            this.filteredFiles = this.removeDuplicate(this.filteredFiles);
            this.$forceUpdate();
        },
    },
});
</script>

<template>
    <div class="body">
        <NavBar />
        <div class="info">
            <h3 class="title">
                A website for all your Tinkers Construct Wiki needs!
            </h3>
            <p class="paragraph">
                Tinkydoc uses the official books as resources so it should be up
                to date, if information is incorrect please contact me via
                Github or Discord
            </p>
        </div>
        <div class="search-parent">
            <input
                v-model="searchQuery"
                class="searchbox"
                type="text"
                placeholder="Search the knowledgebase..."
                @input="searchFiles()"
            />
        </div>
        <p v-if="filteredFiles && searchQuery != ''">
            Results: {{ filteredFiles.length }}
        </p>
        <ul v-if="filteredFiles && searchQuery != ''">
            <li v-for="file in filteredFiles" :key="file">
                <!-- <a :href="`page${file}`">{{ file }}</a>-->
                <RouterLink :to="`/page${file}`">{{ file }}</RouterLink>
                <p>{{ file }}</p>
            </li>
        </ul>
    </div>
</template>
