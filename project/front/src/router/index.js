
import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store/index.js"



Vue.use(VueRouter);


const rejectUser=(to, from, next) =>{

  if(localStorage.getItem("refresh_token")){
    alert("already!")
    next("/")
  }
  else{
    next()
  }

}

const guard=async (to, from, next)=>{
  if (localStorage.getItem("refresh_token")===null){
    alert("login first!")
    next("/login")
  }
  else{
    await store.dispatch("getUserInfo")
    next()
  }
}




const routes = [
  {
    path: "/",
    name: "home",
    beforeEnter: guard,//클릭하면 이거 먼저 실행해서 체크
    component: () =>
    import(/* webpackChunkName: "home" */ "../views/Home.vue")//webpackChunkName 지정하면 해당 이름으로 파일이 분리되어 빌드
  },
  {
    path: "/login",
    name: "login",
    beforeEnter: rejectUser,
    component: () =>
    import(/* webpackChunkName: "login" */ "../views/Login.vue")
  },
  {
    path: "/my_page",
    name: "my_page",
    beforeEnter: guard,
    component: () =>
    import(/* webpackChunkName: "my_page" */ "../views/MyPage.vue")
  },
  {
    path: "/order",
    name: "order",
    beforeEnter: guard,
    component: () =>
    import(/* webpackChunkName: "order" */ "../views/Order.vue")
  },
  {
    path: "/check",
    name: "check",
    beforeEnter: guard,
    component: () =>
    import(/* webpackChunkName: "check" */ "../views/Check.vue")
  },
  {
    path: "/dash_board",
    name: "board",
    beforeEnter: guard,
    component: () =>
    import(/* webpackChunkName: "check" */ "../views/DashBoard.vue")
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
