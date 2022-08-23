import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store";
import HomePage from "@/views/HomePage.vue";
import LoginPage from "@/views/LoginPage.vue";

Vue.use(VueRouter);

// Auth info
const routes = [
  {
    path: "/",
    component: HomePage,
    meta: { requiresAuth: true }
  },
  {
    path: "/login",
    component: LoginPage
  },
  {
    path: "/:catchAll(.*)",
    redirect: "/"
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = store.state.auth.isLoggedIn;
  const token = localStorage.getItem("access");
  console.log("to.path=", to.path);
  console.log("isLoggedIn=", isLoggedIn);

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      console.log("User is not logged in.");
      if (token != null) {
        console.log("Try to renew user info.");
        store
          .dispatch("auth/renew")
          .then(() => {
            console.log("Succeeded to renew. So, free to next.");
            next();
          })
          .catch(() => {
            forceToLoginPage(to);
          });
      } else {
        forceToLoginPage(to);
      }
    } else {
      console.log("User is already logged in. So, free to next.");
      next();
    }
  } else {
    console.log("Go to public page.");
    next();
  }
});

function forceToLoginPage(to) {
  console.log("Force to login page.");
  router.replace({
    path: "/login",
    query: { next: to.fullPath }
  });
}

export default router;
