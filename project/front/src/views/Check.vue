<template>
    <v-container class="ma-10">
        <h2 class="mb-4 font-weight-thin">{{ userInfo.store_name }}점 발주</h2>

        <v-divider class="mb-8"></v-divider>
        <!-- 아이템 나열 -->
    <div class="d-flex flex-column mb-6">
        <v-card
            v-for="item in selectedItems"
            :key="item.id"
            class="pa-3 ma-1"
            outlined
            tile
            max-width="93%"
            :color="'white'"
        >
        <v-row >
            <v-col cols="1" align-self="center">
                <v-checkbox
                :value="item.id"
                @click="item.check=!item.check"
                v-model="checked"
                ></v-checkbox>
            </v-col>
             <v-col cols="4" >
                 <v-row justify="start">
                <h4 class="mt-2" >{{ item.name }}</h4>
                 </v-row>
                <v-row >
                    <p align-self="center">{{ item.info }}</p>
                </v-row>
                <v-row class="mb-1">
                    <v-chip
                        color="indigo lighten-2"
                        text-color="white"
                        >
                        {{item.tag}}
                    </v-chip>
                </v-row>
            </v-col>

            <v-col align-self="center">
                <v-row >
                    <v-col cols="7 text-right" align-self="center"><p>{{item.price}}원</p></v-col>
                    <v-col cols="2" align-self="center" class="text-right">
                        <p>{{item.qty}}</p>
                    </v-col>
                    <v-col align-self="center">
                        <p>{{item.unit}}</p>
                    </v-col>
                        
                </v-row>
            </v-col>

        </v-row>
        <v-divider class="mt-3"></v-divider>
        </v-card>
        <v-col align-self="start" cols="11 text-right" class="my-3">
            <h2>total price</h2>
            <h3 class="mb-6">{{total()}}원</h3>
            
            <v-btn
            color="grey darken-4"
            class="white--text "
            large
            rounded
            @click="newOrder"
            >
                <h3>발주</h3>
                <v-icon
                    right
                    dark
                >
                    mdi-arrow-right-bold
                </v-icon>
            </v-btn>
        </v-col>        
    </div>

  </v-container>
</template>

<script>
import {mapState} from "vuex"
import store from "../store/index.js"
import axios from 'axios'

export default {
  // name: "check",
  data(){
      return {
          selectedItems:[],
          checked:[],
          total_price:0
      }
    },
    computed:{
       
        ...mapState(["userInfo", 'items', 'tags']),
        
    },
    methods:{
        total(){ //총가격저장
            var items=this.items
            var sum=0
            items.forEach(item => {
                if(item.check){
                    sum+=(item.price*item.qty)
                }
             });
            this.total_price=sum
            return sum          
        },
        async newOrder() {
            
            const payload ={
              items:this.selectedItems.filter((item)=>{
                       return this.checked.includes(item.id)
                    }),
              user_key_id:store.state.userInfo.user_key_id,
              store_id:store.state.userInfo.store_id,
              total_price:this.total_price
              //summary
            }

            console.log('payload',payload)
            const path = 'http://localhost:5000/api/order'
            await axios.put(path, payload)
                .then(() => {
                  alert('발주 성공. 홈으로 돌아갑니다 ')
                  console.log("order success")

                  this.$router.push({name: 'home'})
                })
                .catch((error) => {
                console.error(error);
                });
      }
    },
    async created() {
        await store.state.items.forEach(item => {
          if (item.check===true && item.qty>0){
              if(item.qty>item.stock){
                alert('발주 실패::재고 부족 \n홈으로 돌아갑니다 ')
                this.$router.push({name: 'home'})
              }else{
                this.selectedItems.push(item)
                this.checked.push(item.id)
              }

          }
        });
  },
  
};
</script>