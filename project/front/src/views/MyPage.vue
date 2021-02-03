<template>
<div>
    <v-card
        flat
        class="rounded-b-xl indigo lighten-5 mx-10 "
        height="160px"
        >
        <v-row align="center">
            <v-col cols="12" align="center" class="pt-16">
                <h2>{{ userInfo.store_location }}점 발주 내역</h2>
            </v-col>
        </v-row>
        </v-card>

    <div class="ma-10">
        
        <v-divider class="my-5"></v-divider>
        <v-card
            flat
            max-width="100%"
            class="mt-8 pb-2 a-5 rounded-t-xl" 
            v-for="(order, index) in orders"
            :key="index"
            outlined
        >
            <v-toolbar
            :color="'indigo darken-4'"
            dark
            fixed
            height="50px"
            class="rounded-t-xl"
            >

                <v-toolbar-title>
                    {{order.date.slice(0, 22)}}
                </v-toolbar-title>

                <v-spacer></v-spacer>

            </v-toolbar>
            <v-card 
            flat
            max-height="200px"
            class="overflow-y-auto"
            >
            <v-simple-table width="200px"
            >

           <thead>
                <tr>
                    <th class="text-left">
                    Name
                    </th>
                    <th class="text-left">
                    Qty
                    </th>
                    <th class="text-left">
                    Unit
                    </th>
                    <th class="text-left">
                    Price
                    </th>
                    <th class="text-left">
                    Total Price
                    </th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="item in order.order" :key=item.name>
                    <td width="20%">{{item.name}}</td>
                    <td width="20%">{{item.qty}}</td>
                    <td width="20%">{{item.unit}}</td>
                    <td width="20%">{{item.price}}원</td>
                    <td width="20%">{{item.total_price}}원</td>
                </tr>
                 <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td><h4 class="text-left">합계</h4></td>
                    <td>
                    <h4 class="text-left">{{total(index)}}원</h4>
                    </td>
                </tr>
            </tbody>

            </v-simple-table>
            </v-card>
            <v-btn
            large
            dark
            absolute
            bottom
            right
            class="rounded-xl grey darken-4 mb-1 mr-2"
            @click="setItems(index)"
            >
                <v-icon>mdi-cart-arrow-down</v-icon>
            </v-btn>

        </v-card>


    </div>
        
</div>
</template>

<script>
import axios from 'axios';
import store from "../store/index.js"
import {mapState} from "vuex"

export default {
     data(){
        return {
            orders:[]
            
        }
    },
    computed:{
        
        ...mapState(["userInfo"])
    },
    methods:{
        getOrders(){
            const payload ={
                store_id:store.state.userInfo.store_id
            }
            const path = 'http://localhost:5000/api/my_order_info'
             axios.post(path, payload)
              .then((res) => {
                console.log("get my page info")
                this.orders = res.data.order_info
              })
              .catch((error) => {
              console.error(error);
              });
        },
        setItems(index){//store item
            console.log('index',index)
            store.state.items=this.orders[index].order
            this.$router.push({name: 'check'})
        },
        total(index){
            var sum=0
            this.orders[index].order.forEach(item => {
            sum+=(item.price*item.qty)
            })
            return sum
        }
    },
    created(){
        this.getOrders()
    }
};
</script>
