<template>
  <div class="space-detail">
    <van-nav-bar :title="space.name" left-arrow @click-left="$router.back()" fixed>
      <template #right>
        <van-icon name="ellipsis" size="20" />
      </template>
    </van-nav-bar>

    <div class="space-cover">
      <van-image :src="space.cover" fit="cover" width="100%" height="200" />
      <div class="space-overlay">
        <h2>{{ space.name }}</h2>
        <p>{{ space.description }}</p>
      </div>
    </div>

    <div class="space-stats">
      <van-row>
        <van-col span="8" class="stat-item">
          <span class="stat-value">{{ space.itemCount }}</span>
          <span class="stat-label">物品</span>
        </van-col>
        <van-col span="8" class="stat-item">
          <span class="stat-value">{{ space.totalValue }}</span>
          <span class="stat-label">总价值</span>
        </van-col>
        <van-col span="8" class="stat-item">
          <span class="stat-value">{{ space.lastUpdate }}</span>
          <span class="stat-label">更新</span>
        </van-col>
      </van-row>
    </div>

    <van-cell-group inset class="action-group">
      <van-cell title="3D漫游" icon="aim" is-link @click="enterRoaming" />
      <van-cell title="添加物品" icon="add-o" is-link @click="addItem" />
      <van-cell title="空间设置" icon="setting-o" is-link @click="openSettings" />
    </van-cell-group>

    <div class="items-section">
      <div class="section-header">
        <h3>空间物品</h3>
        <van-button type="primary" size="small" plain @click="viewAllItems">查看全部</van-button>
      </div>
      <van-grid :column-num="3" :border="false" :gutter="10">
        <van-grid-item v-for="item in recentItems" :key="item.id" @click="viewItem(item)">
          <van-image :src="item.image" fit="cover" radius="8" width="100%" height="100" />
          <span class="item-name">{{ item.name }}</span>
        </van-grid-item>
      </van-grid>
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
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { showToast } from 'vant';

const router = useRouter();
const route = useRoute();
const activeTab = ref(1);

const space = reactive({
  id: route.params.id,
  name: '客厅',
  description: '家的中心，温暖舒适的休息空间',
  cover: 'https://via.placeholder.com/400x200?text=Living+Room',
  itemCount: 23,
  totalValue: '¥45,230',
  lastUpdate: '2天前'
});

const recentItems = ref([
  { id: 1, name: '沙发', image: 'https://via.placeholder.com/100?text=1' },
  { id: 2, name: '电视柜', image: 'https://via.placeholder.com/100?text=2' },
  { id: 3, name: '茶几', image: 'https://via.placeholder.com/100?text=3' },
  { id: 4, name: '灯具', image: 'https://via.placeholder.com/100?text=4' },
  { id: 5, name: '地毯', image: 'https://via.placeholder.com/100?text=5' },
  { id: 6, name: '装饰画', image: 'https://via.placeholder.com/100?text=6' }
]);

const enterRoaming = () => {
  router.push(`/space/${space.id}/roaming`);
};

const addItem = () => {
  router.push('/scan');
};

const openSettings = () => {
  showToast('设置功能开发中');
};

const viewAllItems = () => {
  router.push('/items');
};

const viewItem = (item) => {
  router.push(`/item/${item.id}`);
};
</script>

<style scoped>
.space-detail { min-height: 100vh; background: #f7f8fa; padding-bottom: 70px; }
.space-cover { position: relative; }
.space-overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 20px; background: linear-gradient(transparent, rgba(0,0,0,0.7)); color: white; }
.space-overlay h2 { font-size: 24px; margin-bottom: 5px; }
.space-stats { background: white; padding: 20px 0; margin-bottom: 10px; }
.stat-item { text-align: center; }
.stat-value { display: block; font-size: 20px; font-weight: bold; color: #333; }
.stat-label { font-size: 12px; color: #999; }
.action-group { margin-bottom: 10px; }
.items-section { background: white; padding: 15px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.item-name { font-size: 12px; margin-top: 5px; text-align: center; }
</style>
