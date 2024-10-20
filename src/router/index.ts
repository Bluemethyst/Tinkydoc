import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import PagePage from "../views/PageView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView,
        },
        {
            path: "/page/:pathMatch(.*)*",
            name: "page",
            // route level code-splitting
            // this generates a separate chunk (About.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            // component: () => import("../views/PagePage.vue"),
            component: PagePage,
        },
    ],
});

export default router;
