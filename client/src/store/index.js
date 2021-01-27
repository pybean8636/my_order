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
    isToken:null
  },
  mutations: {
    //login success
    loginSucceess(state, payload){
      if(state.isToken===true){//login 하고 홈으로 이동...... 을 할라고 한 건데 왜 트루일까
        router.push({name:'home'})
      }
      state.isLogin = true
      state.isLoginError= false
      state.userInfo =payload
      state.isToken = true

      // 
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
      state.userInfo=null
      state.isToken = false
      localStorage.removeItem("access_token")
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
            store_location:response.data.store_location
          }
          commit("loginSucceess", userInfo)
        })
        .catch((error)=>{
          alert(error)
        })

    }

  },//
  modules: {}
});
