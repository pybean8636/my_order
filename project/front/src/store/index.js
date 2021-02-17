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
    items:null,
    tags:null//태그들 정보
  },
  mutations: {
    //login success
    async loginSucceess(state, payload){
      console.log('======')
      
        state.isLogin = true
        state.isLoginError= false
        state.userInfo =payload
        state.isToken = true
        console.log('router',router)
        
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
              let access_token = res.data.access_token
              let refresh_token = res.data.refresh_token
              localStorage.setItem("access_token", access_token)
              localStorage.setItem("refresh_token", refresh_token)
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
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
      router.push({name:'login'})
      console.log('logout')
    },
    getUserInfo({commit}){

      let access_token =localStorage.getItem("access_token")
      let refresh_token =localStorage.getItem("refresh_token")
      let config = {
        headers:{
          "access_Authorization":access_token,
          "refresh_Authorization":refresh_token
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
          localStorage.setItem("access_token", response.data.access_token)
          commit("loginSucceess", userInfo)
        })
        .catch((error)=>{
          console.log(error)
          alert("로그인 실패")
          router.push({name:'login'})
        })

    },
    
    getItems({commit}){
      const payload ={
        store_id: this.state.userInfo.store_id
      }
      const path = 'http://localhost:5000/api/item_info';
          axios.post(path, payload)
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

  },
  modules: {}
});
