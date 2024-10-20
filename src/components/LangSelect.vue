<script lang="ts">
import { defineComponent, inject } from "vue";

export default defineComponent({
    name: "LangSelect",
    setup() {
        const lang = inject("lang");
        return {
            lang,
        };
    },
    methods: {
        changeLang() {
            console.log(this.lang);
        },
    },
});
</script>

<template>
    <div>
        <select v-model="lang" @change="changeLang()">
            <option value="en_us">English</option>
            <option value="ja_jp">Japanese</option>
            <option value="ko_kr">Korean</option>
            <option value="pt_br">Portuguese</option>
            <option value="ru_ru">Russian</option>
            <option value="tr_tr">Turkish</option>
            <option value="zh_cn">Chinese</option>
            <option value="zh_tw">Chinese (Traditional)</option>
        </select>
    </div>
</template>
