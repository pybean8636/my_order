
import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store/index.js"

// const originalPush = VueRouter.prototype.push;
// VueRouter.prototype.push = function push(location) {
//     return originalPush.call(this, location).catch(() => {
//         return window.location.reload()
//     })
// };

Vue.use(VueRouter);

// const onlyUser =async (to, from, next) =>{//로그인 안된 유저의 다른 페이지 접근 막음
//   if(store.state.isLogin===false && store.state.isToken===false){
//     alert("로그인을 해주세요")
//     next("/login")
//   }else{
//     if (to.name==='home'){
//       await store.dispatch("getStoreInfo")
//     }
//     await next()
//   }
// }
// const regectAuthUser =(to, from, next) =>{//로그인 안된 유저의 다른 페이지 접근 막음
//   console.log(store.state.isToken)
//   if(store.state.isToken===true){
//     alert("이미 로그인 되었습니다")
//     next("/")
//   }else{
//     next()
//     console.log('tlqkf')
//   }
// }
// function sleep(ms){
//   var ts1 = new Date().getTime() + ms;
//   do var ts2 = new Date().getTime(); while (ts2<ts1);
// }


const routerGuard=async (to, from, next) =>{
  console.log(store.state)

  // sleep(1000)

  if(to.name!='login' && store.state.isLogin===false && store.state.isToken===false){
    alert("로그인을 해주세요")
    next("/login")
  }
  else if(from.name==='login'&& to.name==='login' && store.state.isLogin===true){
    console.log("durl")
    next("/")
  }
  else if(to.name==='home' && store.state.isToken===true){
    await store.dispatch("getStoreInfo")

    console.log(store.state.storeInfo)
    await next()
  }
  else if(to.name==='login' && store.state.isToken===true){
    alert("이미 로그인 되었습니다")
    next("/")
  }
  else{
    next()
  }


}






const routes = [
  {
    path: "/",
    name: "home",
    beforeEnter: routerGuard,//클릭하면 이거 먼저 실행해서 체크
    component: () =>
    import(/* webpackChunkName: "home" */ "../views/Home.vue")//webpackChunkName 지정하면 해당 이름으로 파일이 분리되어 빌드
  },
  {
    path: "/login",
    name: "login",
    beforeEnter: routerGuard,
    component: () =>
    import(/* webpackChunkName: "login" */ "../views/Login.vue")
  },
  {
    path: "/my_page",
    name: "my_page",
    beforeEnter: routerGuard,
    component: () =>
    import(/* webpackChunkName: "my_page" */ "../views/MyPage.vue")
  },
  {
    path: "/order",
    name: "order",
    beforeEnter: routerGuard,
    component: () =>
    import(/* webpackChunkName: "order" */ "../views/Order.vue")
  },
  {
    path: "/check",
    name: "check",
    beforeEnter: routerGuard,
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
