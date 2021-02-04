<template>
<div class="mx-5">
    <!-- 매장명 -->
    <v-card
        flat
        class="rounded-b-xl indigo lighten-5 mx-10 "
        height="170px"
        max-width="84%"
        >
        <v-row align="center">
            <v-col cols="12" align="center" class="pt-16">
                <h1 class="font-weight-thin">{{ userInfo.store_location }}점 발주 내역</h1>
            </v-col>
        </v-row>
        </v-card>

    <div class="mx-10 mb-8">

        <!-- 정렬 선택 메뉴 -->
        <v-col class="text-right" cols="11">
            <v-menu
            :key="text"
            :rounded="rounded"
            offset-y
            >
            <template v-slot:activator="{ attrs, on }">
                <v-btn
                :color="'grey darken-4'"
                class="white--text mt-8 mx-8"
                v-bind="attrs"
                v-on="on"
                >
                sort options
                </v-btn>
            </template>

            <v-list>
                <v-list-item
                v-for="list in lists"
                :key="list"
                @click="sortBy=list"
                class="text-center"
                >
                <v-list-item-title v-text="list"></v-list-item-title>
                </v-list-item>
            </v-list>
            </v-menu>
        </v-col>

        <!-- 주문 내역 -->
        <v-card
            flat
            max-width="85%"
            class="mt-8 pb-2 mx-8 rounded-t-xl" 
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

                <v-toolbar-title class="mx-4">
                    {{order.date.slice(0, 22)}}
                </v-toolbar-title>

                <v-spacer></v-spacer>

            </v-toolbar>
            <v-card 
            flat
            max-height="200px"
            class="overflow-y-auto px-3"
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
                <tr v-for="item in order.order" :key=item.name class="body-2">
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
                    <td><h4 class="text-left subtitle-2">합계</h4></td>
                    <td>
                    <h4 class="text-left subtitle-2">{{order.sum}}원</h4>
                    </td>
                </tr>
            </tbody>

            </v-simple-table>
            </v-card>
            <!-- 똑같이 발주 버튼 -->
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
            orders:[],//주문 내역
            lists:['최신순', '금액순'],//정렬 기준 list
            sortBy:'최신순'//정렬 기준 default:최신순   
            
        }
    },
    computed:{
        
        ...mapState(["userInfo"])//사용자 정보
    },
    methods:{
        getOrders(){//그동안 사용자의 매장 발주 내역 가져오기
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
        setItems(index){//store item에 똑같이 주문할 아이템 정보 저장
            console.log('index',index)
            store.state.items=this.orders[index].order
            this.$router.push({name: 'check'})
        },

        customSort(i, j){//sorting custom
            if (this.sortBy==='최신순'){
                if(i.date===j.date){
                    return 0
                }
                return i.date< j.date? 1:-1
            }
            else{
                if(i.sum===j.sum){
                    return 0
                }
                return i.sum< j.sum? 1:-1
            }
            
        }
            

    },
    created(){
        this.getOrders()//주문 내역 가져오기
    },
    watch:{//order sorting
        sortBy(newV, oldV){
            if (oldV!=newV){
                this.orders.sort(this.customSort)
            }
        }
    }
};
</script>
