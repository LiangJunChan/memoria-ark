<template>
  <div class="spaces-view">
    <van-nav-bar title="我的空间" fixed>
      <template #right>
        <van-icon name="plus" size="20" @click="createSpace" />
      </template>
    </van-nav-bar>

    <div class="spaces-content">
      <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
        <van-list
          v-model:loading="loading"
          :finished="finished"
          finished-text="没有更多了"
          @load="onLoad"
        >
          <div v-for="space in spaces" :key="space.id" class="space-card" @click="enterSpace(space)">
            <van-image :src="space.cover" fit="cover" class="space-cover" />
            <div class="space-info">
              <h3>{{ space.name }}</h3>
              <p>{{ space.itemCount }}件物品 · {{ space.description }}</p>
            </div>
            <van-icon name="arrow" class="enter-icon" />
          </div>
        </van-list>
      </van-pull-refresh>
    </div>

    <van-tabbar v-model="activeTab" route>
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="apps-o" to="/spaces">空间</van-tabbar-item>
      <van-tabbar-item icon="scan" to="/scan"></van-tabbar-item>
      <van-tabbar-item icon="medal-o" to="/achievements">成就</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';

const router = useRouter();
const activeTab = ref(1);
const loading = ref(false);
const finished = ref(false);
const refreshing = ref(false);

const spaces = ref([
  { id: 1, name: '客厅', itemCount: 23, description: '主要活动区域', cover: 'https://via.placeholder.com/400x200?text=Living+Room' },
  { id: 2, name: '卧室', itemCount: 15, description: '休息空间', cover: 'https://via.placeholder.com/400x200?text=Bedroom' },
  { id: 3, name: '书房', itemCount: 42, description: '工作和学习', cover: 'https://via.placeholder.com/400x200?text=Study' },
  { id: 4, name: '厨房', itemCount: 18, description: '烹饪空间', cover: 'https://via.placeholder.com/400x200?text=Kitchen' }
]);

const onLoad = () => {
  setTimeout(() => {
    finished.value = true;
  }, 500);
};

const onRefresh = () => {
  setTimeout(() => {
    refreshing.value = false;
    showToast('刷新成功');
  }, 500);
};

const enterSpace = (space) => {
  router.push(`/space/${space.id}`);
};

const createSpace = () => {
  router.push('/spaces/create');
};
</script>

<style scoped>
.spaces-view { min-height: 100vh; background: #f7f8fa; padding-bottom: 70px; }
.spaces-content { padding-top: 46px; }
.space-card { background: white; margin: 10px; border-radius: 12px; overflow: hidden; position: relative; }
.space-cover { width: 100%; height: 120px; }
.space-info { padding: 12px; }
.space-info h3 { font-size: 16px; margin-bottom: 4px; }
.space-info p { font-size: 12px; color: #666; }
.enter-icon { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); color: #999; }
</style>