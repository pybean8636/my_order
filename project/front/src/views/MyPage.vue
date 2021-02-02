<template>
    <div class="ma-10">
        <h2>{{ userInfo.store_location }}점 발주 내역</h2>
        <!-- 나중에 매장아이디로 바꿔서 같은 매장 주문내역 공유 -->
        
        <v-divider class="my-5"></v-divider>
        <v-card
            elevation="2"
            max-width="100%"
            class="mt-8 pb-2 a-5"
            v-for="(order, index) in orders"
            :key="index"
        >
            <v-toolbar
            :color="'grey darken-2'"
            dark
            fixed
            height="50px"
            >

                <v-toolbar-title>
                    {{order.date}} Order List
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
                    <td>{{item.name}}</td>
                    <td>{{item.qty}}</td>
                    <td>{{item.unit}}</td>
                    <td>{{item.price}}</td>
                    <td>{{item.total_price}}</td>
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
            class="v-btn--example grey darken-3"
            @click="setItems(index)"
            >
                <v-icon>mdi-cart-arrow-down</v-icon>
            </v-btn>

        </v-card>




        <!-- <v-card
            elevation="2"
            width="900px"
            class="m7-8"
        >
            <v-toolbar
            :color="'grey darken-2'"
            class="mb-1"
            dark
            >

            <v-toolbar-title>
                Order List
            </v-toolbar-title>
            </v-toolbar>

                <v-treeview
                activatable
                color="warning"
                :items="items"
                >
                </v-treeview>

            
            </v-card> -->

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
        }
    },
    created(){
        this.getOrders()
    }
};
</script>
