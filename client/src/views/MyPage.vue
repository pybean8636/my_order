<template>
    <div>
        <h2>{{ userInfo.id }}의 발주 내역</h2>
        <!-- 나중에 매장아이디로 바꿔서 같은 매장 주문내역 공유 -->
    </div>
</template>

<script>
import {mapState} from "vuex"

export default {
  computed:{
      ...mapState(["userInfo"])
  }
};
</script>
