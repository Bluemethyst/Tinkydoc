<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "NavBar",
    setup() {
        return {};
    },
});
</script>

<template>
    <nav>
        <h1 id="nav-title" class="title">Tinkydoc</h1>
        <div class="router-links">
            <RouterLink class="router-link" to="/">Home</RouterLink>
            <RouterLink class="router-link" to="/page">Page</RouterLink>
        </div>
    </nav>
</template>
