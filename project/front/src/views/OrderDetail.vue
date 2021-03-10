<template>
    <div class="ma-10 pa-4">
        <div id="title" class="ml-5">
            <h2 class="mb-4 font-weight-thin">{{ userInfo.store_name }}점 발주 상세</h2>
            <v-divider class="my-8" max-width="90%"></v-divider>
        </div>
        <div id="item-list" class="mt-10">
            <v-toolbar
            color="indigo lighten-5"
            class="rounded-t-xl pa-3 mx-3 my-8"
            height="90px"
            max-width="93%"
            flat
            >
                <v-col cols="6" class="pl-10 pb-8">
                    <h3>발주 날짜 {{items[0].date}}</h3>
                </v-col>
                <v-col class="text-right pb-8" cols="5">
                    <h3>주문자 {{items[0].user_id}}</h3>
                </v-col> 
            </v-toolbar>
            <v-card
            v-for="item in items"
            :key="item.id"
            class="pa-3 ma-1"
            outlined
            tile
            max-width="93%"
            :color="'white'"
            >
            <v-row >
                <v-col cols="1" align-self="center">
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
            outlined
            text
            rounded
            dark
            large
            class="grey darken-4"
            @click="setItems()"
            >
                <h3>발주-></h3>
            </v-btn>
            </v-col>    
            
        </div>
    </div>
</template>

<script>
import {mapState} from "vuex"
import store from "../store/index.js"

export default {
    name:"detail",
    data(){
        return{
            items:[],
            total_price:0 
        }
    },
    computed:{
        ...mapState(["userInfo"])
    },
    methods:{
        total(){ //총가격저장
            var items=this.items
            var sum=0
            items.forEach(item => {
                sum+=item.total_price
             });
            this.total_price=sum
            return sum          
        },
        setItems(){
            store.state.items=this.items
            this.$router.push({name: 'check'})
        }
    },
    mounted(){
        this.items=store.state.items
    }
}
</script>