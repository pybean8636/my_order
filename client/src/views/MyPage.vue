<template>
    <div class="ma-10">
        <h2>{{ userInfo.store_location }}점 발주 내역</h2>
        <!-- 나중에 매장아이디로 바꿔서 같은 매장 주문내역 공유 -->
        
        <v-card
            elevation="2"
            max-width="100%"
            class="mt-8 pb-2 a-5"
        >
            <v-toolbar
            :color="'grey darken-2'"
            dark
            fixed
            height="50px"
            >

                <v-toolbar-title>
                    2021-01-19 17:30:00 Order List
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
                <th class="text-left ">
                    <div class="body-2 font-weight-bold">Name</div>
                </th>
                <th class="text-left">
                Qty
                </th>
                <th class="text-left">
                Unit
                </th>
                <th class="text-left">
                Total Price
                </th>
            </tr>
            </thead>

            <tbody>
            <tr>
                <td>item</td>
                <td>qty</td>
                <td>box</td>
                <td>price</td>
            </tr>


            <tr>
                <td>item</td>
                <td>qty</td>
                <td>box</td>
                <td>price</td>
            </tr>
            <tr>
                <td>item</td>
                <td>qty</td>
                <td>box</td>
                <td>price</td>
            </tr>
            <tr>
                <td>item</td>
                <td>qty</td>
                <td>box</td>
                <td>price</td>
            </tr>
            <tr>
                <td>item</td>
                <td>qty</td>
                <td>box</td>
                <td>price</td>
            </tr>
            <tr>
                <td>item</td>
                <td>qty</td>
                <td>box</td>
                <td>price</td>
            </tr>
            <tr>
                <td>item</td>
                <td>qty</td>
                <td>box</td>
                <td>price</td>
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
            @click="$router.push({name: 'check'})"
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
import {mapState} from "vuex"

export default {
     data(){
        return {
            tag:false,
            items: [
                {
                id: 1,
                name: 'Applications :',
                children: [
                    { id: 2, name: 'Calendar : app' },
                    { id: 3, name: 'Chrome : app' },
                    { id: 4, name: 'Webstorm : app' },
                ],
                },
                {
                id: 5,
                name: 'Documents :',
                children: [
                    {
                    id: 6,
                    name: 'vuetify :',
                    children: [
                        {
                        id: 7,
                        name: 'src :',
                        children: [
                            { id: 8, name: 'index : ts' },
                            { id: 9, name: 'bootstrap : ts' },
                        ],
                        },
                    ],
                    },
                    {
                    id: 10,
                    name: 'material2 :',
                    children: [
                        {
                        id: 11,
                        name: 'src :',
                        children: [
                            { id: 12, name: 'v-btn : ts' },
                            { id: 13, name: 'v-card : ts' },
                            { id: 14, name: 'v-window : ts' },
                        ],
                        },
                    ],
                    },
                ],
                },
                {
                id: 15,
                name: 'Downloads :',
                children: [
                    { id: 16, name: 'October : pdf' },
                    { id: 17, name: 'November : pdf' },
                    { id: 18, name: 'Tutorial : html' },
                ],
                },
                {
                id: 19,
                name: 'Videos :',
                children: [
                    {
                    id: 20,
                    name: 'Tutorials :',
                    children: [
                        { id: 21, name: 'Basic layouts : mp4' },
                        { id: 22, name: 'Advanced techniques : mp4' },
                        { id: 23, name: 'All about app : dir' },
                    ],
                    },
                    { id: 24, name: 'Intro : mov' },
                    { id: 25, name: 'Conference introduction : avi' },
                ],
                },
            ]
        }
    },
    computed:{
        
        ...mapState(["userInfo"])
    }
};
</script>
