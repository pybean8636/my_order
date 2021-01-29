// import { false } from "tap";
// import { false } from "tap";
import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store/index.js"

Vue.use(VueRouter);

const onlyUser =(to, from, next) =>{//로그인 안된 유저의 다른 페이지 접근 막음
  if(store.state.isLogin===false && store.state.isToken===false){
    alert("로그인을 해주세요")
    next("/login")
  }else{
    next()
  }
}
const regectAuthUser =(to, from, next) =>{//로그인 안된 유저의 다른 페이지 접근 막음
  if(store.state.isToken===true){
    alert("이미 로그인 되었습니다")
    next("/")
  }else{
    next()
    console.log('tlqkf')
  }
}

const routes = [
  {
    path: "/",
    name: "home",
    beforeEnter: onlyUser,//클릭하면 이거 먼저 실행해서 체크
    component: () =>
    import(/* webpackChunkName: "home" */ "../views/Home.vue")//webpackChunkName 지정하면 해당 이름으로 파일이 분리되어 빌드
  },
  {
    path: "/login",
    name: "login",
    beforeEnter: regectAuthUser,
    component: () =>
    import(/* webpackChunkName: "login" */ "../views/Login.vue")
  },
  {
    path: "/my_page",
    name: "my_page",
    beforeEnter: onlyUser,
    component: () =>
    import(/* webpackChunkName: "my_page" */ "../views/MyPage.vue")
  },
  {
    path: "/order",
    name: "order",
    beforeEnter: onlyUser,
    component: () =>
    import(/* webpackChunkName: "order" */ "../views/Order.vue")
  },
  {
    path: "/check",
    name: "check",
    beforeEnter: onlyUser,
    component: () =>
    import(/* webpackChunkName: "check" */ "../views/Check.vue")
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
