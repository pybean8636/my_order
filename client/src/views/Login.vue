<template>
   <v-container fill-height style="max-width:450px;">
       <v-layout align-center row wrap>
           <v-flex xs12>
               <v-alert 
               type="error"
               :value="isError"
               class="mb-1"
               >
                login fail
                </v-alert>
               <v-card>
                   <v-toolbar
                    dark
                    color="grey"
                    flat
                    >
                        <v-toolbar-title>
                            Login
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
                        @keyup.enter="login()"
                        >
                        </v-text-field>
                    </div>
                    <div class="text-center pa-3"> 
                        <v-hover
                            open-delay="400"
                            color="grey"
                        >
                            <v-btn 
                            rounded
                            dark
                            block
                            @click="login()"
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
export default {
    data(){
        return {
            id:null,
            pw:null,
            isError:false
        }
    },
    methods:{
        login(){
            let selectedUser=null
            this.allUsers.forEach(user => {
                if(user.id === this. id) selectedUser=user    
            });
            selectedUser===null ? this.isError = true :
                selectedUser.pw != this.pw ? this.isError = true : console.log('login success')
        }
    }
}
</script>