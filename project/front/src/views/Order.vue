<template>
    <v-container class="ma-8" max-width="90%">
        <v-card 
        class="rounded-t-xl pa-10 indigo lighten-5"
        flat
        > 
        <h1 class="text-center font-weight-thin mt-5">{{ userInfo.store_location }}점 발주</h1>
        
    <!-- 스위치 -->
      <v-switch
            label="태그별 모아보기 "
            color="indigo"
            value="success"
            hide-details
            shaped
            @click="tag = !tag"
            left
        ></v-switch>

        <!-- 태그선택 슬라이드 시트 -->
        <v-sheet
        v-if="tag"
        class="mt-6 indigo lighten-5"
         >
            <v-slide-group
            multiple
            show-arrows
            v-model="model" 
            >
                <v-slide-item
                    v-for="tag in tags"
                    :key="tag"
                    :value="tag"
                    v-slot="{ active, toggle }"
                >
                <!-- 모델에 선택된 태그들로 필터링하기 위해서 태그 이름을 값으로 배열에 저장 -->
                    <v-btn
                    class="mx-2"
                    :input-value="active"
                    active-class="indigo darken-4 white--text"
                    depressed
                    rounded
                    @click="toggle"
                    >
                    <!-- 태그 받아와야 함~! -->
                    {{ tag }}
                    </v-btn>
                </v-slide-item>
            </v-slide-group>
        </v-sheet>
</v-card>
        <v-divider class="mb-8"></v-divider>
        <!-- 아이템 나열 -->
        <!-- <p>{{ model }}</p> -->
    <div class="d-flex flex-column mb-6">
        <v-card
            v-for="item in filterByTag"
            :key="item.id"
            class="pa-3 ma-1"
            outlined
            tile
            max-width="100%"
            :color="item.check? 'indigo lighten-5' : 'white'"
        >
        <!-- 재고 있는 아이템 -->
        <v-row 
        v-if="item.stock>10"
        >
            <v-col cols="1" align-self="center">
                <v-checkbox
                :value="item.id"
                @click="item.check=!item.check"
                v-model="selected"
                ></v-checkbox>
                
            </v-col>

             <v-col cols="4" >
                 <v-row justify="start">
                <h4 class="mt-2 " >{{ item.name }}</h4>
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
                    <v-col cols="6 text-right" align-self="center">{{item.price}}원</v-col>
                    <v-col cols="3" align-self="center">
                        <v-text-field
                            min="0"
                            type="number"
                            :value="item.qty"
                            v-model.number="item.qty"
                            :on="item.qty> item.stock ? alert2(item.id) : true "
                        ></v-text-field>
                    </v-col>
                    <v-col align-self="center">
                        <p>{{item.unit}}</p>
                    </v-col>
                        
                </v-row>
            </v-col>

        </v-row>
        <!-- 재고부족 -->
        <v-row 
        v-else
        >
            <v-col cols="1" align-self="center">
                <v-checkbox
                :value="item.id"
                disabled
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
                <v-row align="center">
                    
                    <v-col cols="12 text-center"><p class="headline ">SOLD OUT</p></v-col>
                    <!-- <v-col cols="2" align-self="center">
                        
                    </v-col>
                    <v-col align-self="center">
                        
                    </v-col> -->
                        
                </v-row>
            </v-col>

        </v-row>
        <v-divider class="mt-3"></v-divider>
        </v-card>
        <v-col align-self="start" cols="11 text-right" class="my-3">
            <h2>total price</h2>
            <h3 class="mb-6">{{total}}원</h3>
            <v-btn
            color="grey darken-4"
            class="white--text "
            large
            rounded
            @click="$router.push({name: 'check'})"
            >
                선택 완료
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
import {mapState, mapActions} from "vuex"
import store from "../store/index.js"

export default {
     data(){
        return {
            model:null, //선택된 태그 저장
            tag:false, //태그별 보기 필터링
            selected:[]
            
        }
    },
    computed:{
        
        ...mapState(["userInfo", 'items', 'tags']),
        total(){ //총가격저장
            var items=this.items
            var sum=0
            items.forEach(item => {
                if(item.check){
                    sum+=(item.price*item.qty)
                }
             });
            return sum          
        },
        filterByTag(){//태그별 보기
            if (this.tag===true && this.model!=null && this.model.length>0){
                return this.items.filter((item)=>{
                    return this.model.includes(item.tag)
                })
            }else{
                return this.items
            }
        }
        
    },
    methods:{
        ...mapActions(['getItems']),//발주 할 수 있는 아이템 가져옴
        alert2(id){//재고 초과시 알림 
            alert('주문 가능 수량 초과\n주문 가능한 최대 수량으로 자동 수정됩니다.')
            this.items.forEach(item => {
                if(item.id===id){
                    item.qty=item.stock
                }
                
            });
        }

        
    },

    created() {
        store.dispatch('getItems')
        // this.outOfStock()
  },
};
</script>
