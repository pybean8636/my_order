<template>
<!-- my page -->
    <div class="mx-5">
        <div id="title">
            <v-card
            flat
            class="rounded-b-xl indigo lighten-5 mx-10 "
            height="170px"
            max-width="84%"
            >
                <v-row align="center">
                    <v-col cols="12" align="center" class="pt-16">
                        <h1 class="font-weight-thin">{{ userInfo.store_name}}점 발주 내역</h1>
                    </v-col>
                </v-row>
            </v-card>
        </div>
        <div id="sort-button">
            <v-col class="text-right pr-13" cols="11">
                <v-menu
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
        </div>
        <div id="order-list" class="mx-8">
            <v-card 
            v-for="(order, index) in paginatedData"
            :key="index"
            class="indigo lighten-5 ma-6"
            height="80px"
            max-width="85%"
            flat
            >
                <!-- {{order}} -->
                <v-container fluid>
                    <v-row justify="center" align="center" class="pt-2">
                        <v-col align-self="center" cols="3" class="text-center pl-4">
                            발주날짜: {{order.date}}
                        </v-col>
                        <v-col align-self="center" cols="3" class="text-center">
                            {{order.summary}}
                        </v-col>
                        <v-col align-self="center" cols="2" class="text-center">
                            {{order.total_price}}원
                        </v-col>
                        <v-col align-self="center" cols="2" class="text-center">
                            주문자 {{order.user_id}}
                        </v-col>
                        <v-col cols="2" class="text-center">
                            <v-btn
                            outlined
                            text
                            dark
                            class="indigo darken-3 text-center"
                            @click="setItems(order.order_id)"
                            >
                                자세히
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card>
            <div id="pagination">
                <div class="text-center my-5">
                    <v-col cols="11">
                        <v-pagination
                        v-model="pageNum"
                        :length="pageCount"
                        ></v-pagination>
                    </v-col>
                    
                </div>
            </div>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios';
import store from "../store/index.js"
import {mapState} from "vuex"

export default {
    name: "my_page",
    data(){
        return{
            orders:[],
            lists:['최신순', '금액순'],//정렬 기준 list
            sortBy:'최신순',//정렬 기준 default:최신순
            
            pageNum :1,//현재 페이지
            pageSize:6,//한 페이지에 나올 발주 정보 사이즈
        }
    },
    computed:{
        ...mapState(["userInfo"]),
        pageCount(){//페이지 개수
            let order_length=this.orders.length,
            listSize= this.pageSize,
            page=Math.floor((order_length-1)/listSize)+1;

            return page;
        },
        paginatedData(){//페이지 별로 슬라이스
            const start = (this.pageNum -1) * this.pageSize,
            end= start + this.pageSize;

            return this.orders.slice(start, end);
        }
    },
    methods:{
        getOrders(){//매장 발주 내역 가져오기
            const payload ={
                store_id:store.state.userInfo.store_id
            }
            const path = 'http://localhost:5000/api/my_page'
            axios.post(path, payload)
            .then((res) => {
                this.orders = res.data.order_info
            })
            .catch((error) => {
            console.error(error);
            });
        },
        async getDetails(order_id){
            const payload={
                order_id: order_id
            }
            const path = 'http://localhost:5000/api/order_detail'
            await axios.post(path, payload)
            .then((res) => {
                 store.state.items = res.data.detail_info
            })
            .catch((error) => {
            console.error(error);
            });
        },
        async setItems(order_id){//store item에 똑같이 주문할 아이템 정보 저장
            await this.getDetails(order_id)
            this.$router.push({name: 'detail'})
        },
        customSort(i, j){//sorting custom
            if (this.sortBy==='최신순'){
                if(i.date===j.date){
                    return 0
                }
                return i.date < j.date? 1:-1
            }
            else{
                if(i.total_price===j.total_price){
                    return 0
                }
                return i.total_price< j.total_price? 1:-1
            }
            
        },
        // nextPage(){
        //     this.pageNum+=1;
        // },
        // prevPage(){
        //     this.pageNum-=1;
        // }
    },
    mounted(){
        this.getOrders()
    },
    watch:{//order sorting
        async sortBy(newV, oldV){
            if (oldV!=newV){
                await this.orders.sort(this.customSort)
                this.pageNum=1
            }
        }
    }
}
</script>