import { ref, provide, inject } from "vue";

const langSymbol = Symbol();

export function provideLang() {
    const lang = ref("en_us");
    provide(langSymbol, lang);
    return lang;
}

export function useLang() {
    const lang = inject(langSymbol);
    if (!lang) {
        throw new Error("useLang must be used after provideLang");
    }
    return lang;
}
