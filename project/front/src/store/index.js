import Vue from "vue";
import Vuex from "vuex";
import router from "../router";
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLogin: false,
    isLoginError:false,
    userInfo:null,
    isToken:null,
    storeInfo:null,
    items:null,
    tags:null
  },
  mutations: {
    //login success
    async loginSucceess(state, payload){
      console.log('======')
      // if(state.isLogin===false && state.isToken !=true){
      //   console.log('first login',state.isToken, state.isLogin)
      //   state.isLogin = true
      //   state.isLoginError= false
      //   state.userInfo =payload
      //   state.isToken = true
      //   console.log('======',state.isToken, state.isLogin)

      //   await router.push({name:'home'})//js 비동기 잊지 말고 순서 중요한거 async걸기
      // }else{
        // console.log('ntimes login',state.isToken, state.isLogin)
        state.isLogin = true
        state.isLoginError= false
        state.userInfo =payload
        state.isToken = true
        console.log('router',router)
        
        // await router.push({name:'home'})
      // }
      // // 
    },
    //login fail
    loginError(state){
      state.isLogin = false
      state.isLoginError= true
      state.isToken = false
    },
    quitAuth(state){
      state.isLogin=false
      state.isLoginError= false
      state.isToken = null
      state.userInfo=null
      state.storeInfo=null
      localStorage.removeItem("access_token")
    },
    getStoreSucceess(state, payload){

      state.storeInfo=payload

    },
    getItemSucceess(state, payload){

      state.items=payload.itemInfo
      state.tags=payload.tagInfo
      // console.log(state.items)
    }
  },//change state
  actions: {
    //tryng login  success->loginSuccess commit, fail->loginError commit
    login({dispatch}, loginOb){
        const path = 'http://localhost:5000/api/auth/login';
        axios
            .post(path, loginOb)
            .then((res) => {
              let token = res.data.token
              localStorage.setItem("access_token", token)
              dispatch("getUserInfo")//action 실행은 dispatch
              console.log('login post')
        })
        .catch((error) => {
            console.error(error);
            dispatch("loginError")
        })
    },
    logout({commit}){
      commit('quitAuth')
      router.push({name:'login'})
      console.log('logout')
    },
    getUserInfo({commit}){

      let token =localStorage.getItem("access_token")
      let config = {
        headers:{
          "Authorization":token
        }
      }
      console.log(config)
      const path = 'http://localhost:5000/api/user_info';
      axios
        .get(path, config)
        .then(response =>{
          let userInfo = {
            id:response.data.user_id,
            name:response.data.user_name,
            contact:response.data.user_contact,
            store_id:response.data.store_id,
            store_location:response.data.store_location,
            user_key_id:response.data.user_key_id
          }
          commit("loginSucceess", userInfo)
        })
        .catch((error)=>{
          console.log(error)
          alert("로그인 실패")
          router.push({name:'login'})
        })

    },
    getStoreInfo({commit}){

      let token =localStorage.getItem("access_token")
      let config = {
        headers:{
          "Authorization":token
        }
      }
      console.log(config)
      const path = 'http://localhost:5000/api/store_info';
      axios
        .get(path, config)
        .then(async response =>{
          let storeInfo = {
            location:response.data.store_location,
            contact:response.data.store_contact,
            headquarters:response.data.headquarters_name 
          }
          // console.log(storeInfo)
         commit("getStoreSucceess", storeInfo)
        })
        .catch((error)=>{
          console.log(error)
          alert("매장정보 가져오기 실패")
        })

    },
    getItems({commit}){

      let token =localStorage.getItem("access_token")
      let config = {
        headers:{
          "Authorization":token
        }
      }
      console.log(config)
      const path = 'http://localhost:5000/api/item_info';
          axios.get(path, config)
              .then((response) => {
              let info={
                itemInfo:response.data.item_info,
                tagInfo:response.data.tags
              }
              commit("getItemSucceess", info)
              })
              .catch((error) => {
              console.error(error);
              });

    }

  },//
  modules: {}
});
