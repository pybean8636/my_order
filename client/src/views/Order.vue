<template>
    <div>
      <v-switch
            v-model="ex11"
            label=" 태그별 모아보기 "
            color="success"
            value="success"
            hide-details
            @click="tag = !tag"
            class="mb-5"
        ></v-switch>
        <v-sheet
        max-width="900"
        v-if="tag"
        class="mb-5"
         >
            <v-slide-group
            multiple
            show-arrows
            >
                <v-slide-item
                    v-for="n in 10"
                    :key="n"
                    v-slot="{ active, toggle }"
                >
                    <v-btn
                    class="mx-2"
                    :input-value="active"
                    active-class="purple white--text"
                    depressed
                    rounded
                    @click="toggle"
                    >
                    Options {{ n }}
                    </v-btn>
                </v-slide-item>
            </v-slide-group>
        </v-sheet>
    </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "order",
  data(){
      return{

            tag:false,
      }
  },
  components: {
  }
};
</script>
