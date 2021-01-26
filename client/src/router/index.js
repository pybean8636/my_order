import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: () =>
    import(/* webpackChunkName: "home" */ "../views/Home.vue")//webpackChunkName 지정하면 해당 이름으로 파일이 분리되어 빌드
  },
  {
    path: "/login",
    name: "login",
    component: () =>
    import(/* webpackChunkName: "login" */ "../views/Login.vue")
  },
  {
    path: "/my_page",
    name: "my_page",
    component: () =>
    import(/* webpackChunkName: "my_page" */ "../views/MyPage.vue")
  },
  {
    path: "/order",
    name: "order",
    component: () =>
    import(/* webpackChunkName: "order" */ "../views/Order.vue")
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
