<template>
   <v-container fill-height style="max-width:450px;">
       <v-layout align-center row wrap>
           <v-flex xs12>
               <v-alert 
               type="error"
               :value="isLoginError"
               class="mb-1"
               >
                login fail
                </v-alert>
               <v-card>
                   <v-toolbar
                    color="indigo lighten-5"
                    flat
                    >
                        <v-toolbar-title>
                            <h3>Login</h3>
                        </v-toolbar-title>
                    </v-toolbar>
                    <div class="pa-5" >
                        <v-text-field
                        v-model="id"
                        label="ID"
                        placeholder="ID를 입력해주세요"
                        outlined
                        >
                        </v-text-field>
                        <v-text-field
                        v-model="pw"
                        label="PW"
                        type="password"
                        placeholder="PW를 입력해주세요"
                        outlined
                        @keyup.enter="login({id:id,pw:pw})"
                        >
                        </v-text-field>
                    </div>
                    <div class="text-center pa-3"> 
                        <v-hover
                            open-delay="400"
                        >
                            <v-btn 
                            dark
                            block
                            @click="login({id:id,pw:pw})"
                            class="grey darken-4"
                            >
                                로그인  
                            </v-btn>
                        </v-hover>
                    </div>
                </v-card>
           </v-flex>
       </v-layout>
   </v-container>
</template>


<script>
import {mapState, mapActions} from "vuex"

export default {
    data(){
        return {
            id:null,
            pw:null,
        }
    },
    computed:{
        ...mapState(['isLogin', 'isLoginError'])
    },
    methods:{
        ...mapActions(['login']),
    },
    watch:{
        isLogin(newV, oldV){
            if (oldV!=true && newV===true){
                this.$router.push({name: 'home'})
            }
        }
    }
}
</script>