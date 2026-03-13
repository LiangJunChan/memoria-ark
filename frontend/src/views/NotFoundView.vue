<template>
  <div class="not-found">
    <van-nav-bar
      title="页面未找到"
      left-arrow
      @click-left="$router.back()"
    />
    <div class="content">
      <van-icon name="warning-o" size="80" color="#ff976a" />
      <h2>404</h2>
      <p>抱歉，您访问的页面不存在</p>
      <van-button type="primary" round @click="goHome">返回首页</van-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goHome = () => {
  router.push('/');
};
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  background: #f7f8fa;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.content h2 {
  font-size: 48px;
  color: #ff976a;
  margin: 20px 0 10px;
}

.content p {
  color: #666;
  margin-bottom: 30px;
}

.van-button {
  width: 200px;
}
</style>