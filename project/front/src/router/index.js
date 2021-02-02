
import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store/index.js"



Vue.use(VueRouter);


// const routerGuard=(to, from, next) =>{
//   // if (to.name=='login' && store.state.isToken)
//   if (to.name!='login' &&store.state.isToken===false){
//     alert("로그인을 해주세요!")
//     next("/login")
//   }else if(to.name==='login'&& store.state.isLogin===true){
//     alert("이미 로그인 되었습니다!")
//     store.dispatch("getUserInfo").then(()=>{
//       next("/")
//     })
//   }
//   // else if(to.name===from.name){
//   //   console.log('refresh')
//   // }
//   else{
//     store.dispatch("getUserInfo").then(()=>{
//       next()
//     })
//     // store.dispatch("getStoreInfo").then(()=>{
//     //   next("/")
//     // })
//     // store.dispatch("getUserInfo").then(()=>{

//     //   if(to.name!='login' && store.state.isLogin===false && store.state.isToken===false){
//     //     alert("로그인을 해주세요")
//     //     next("/login")
//     //   }
//     //   else if(from.name==='login'&& to.name==='login' && store.state.isLogin===true){
//     //     console.log("home 이동")
//     //     next("/")
//     //   }
//     //   else if(to.name==='home' && store.state.isToken===true){
//     //     store.dispatch("getStoreInfo")
    
//     //     console.log(store.state.storeInfo)
//     //     next()
//     //   }
//     //   else if(to.name==='login' && store.state.isToken===true){
//     //     alert("이미 로그인 되었습니다")
//     //     next("/")
//     //   }
//     //   else{
//     //     next()
//     //   }

//     // })
//   }

// }

const rejectUser=(to, from, next) =>{

  if(store.state.isToken===true){
    alert("already!")
    next("/")
  }
  else{
    next()
  }


}

const guard=(to, from, next)=>{
  if (store.state.isToken===false){
    alert("login first!")
    next("/login")
  }
  else{
    store.dispatch("getUserInfo")
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
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
