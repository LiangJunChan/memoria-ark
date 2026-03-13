<template>
  <div class="home-view">
    <!-- 顶部搜索栏 -->
    <div class="search-header">
      <van-search
        v-model="searchKeyword"
        placeholder="搜索物品、空间..."
        @search="onSearch"
      />
      <van-icon name="scan" class="scan-icon" @click="goToScan" />
    </div>

    <!-- 快捷入口 -->
    <div class="quick-actions">
      <van-grid :column-num="4" :border="false">
        <van-grid-item icon="add-o" text="添加物品" @click="goToAddItem" />
        <van-grid-item icon="photo-o" text="拍照识别" @click="goToScan" />
        <van-grid-item icon="apps-o" text="空间管理" @click="goToSpaces" />
        <van-grid-item icon="chart-trending-o" text="数据分析" @click="goToStats" />
      </van-grid>
    </div>

    <!-- 最近添加 -->
    <div class="section recent-items">
      <div class="section-header">
        <h3>最近添加</h3>
        <van-button type="primary" size="small" plain @click="goToItems">查看全部</van-button>
      </div>
      <div class="items-list">
        <van-card
          v-for="item in recentItems"
          :key="item.id"
          :title="item.name"
          :thumb="item.image"
          @click="viewItem(item)"
        >
          <template #desc>
            <div class="item-meta">
              <van-tag type="primary" size="small">{{ item.category }}</van-tag>
              <span class="item-location">
                <van-icon name="location-o" /> {{ item.space }}
              </span>
            </div>
          </template>
          <template #price>
            <span class="item-price">{{ item.price }}</span>
          </template>
        </van-card>
      </div>
    </div>

    <!-- 空间概览 -->
    <div class="section spaces-overview">
      <div class="section-header">
        <h3>我的空间</h3>
        <van-button type="primary" size="small" plain @click="goToSpaces">管理</van-button>
      </div>
      <div class="spaces-grid">
        <div
          v-for="space in spaces"
          :key="space.id"
          class="space-card"
          :style="{ backgroundImage: `url(${space.cover})` }"
          @click="enterSpace(space)"
        >
          <div class="space-overlay">
            <h4>{{ space.name }}</h4>
            <p>{{ space.itemCount }} 件物品</p>
          </div>
        </div>
        <div class="space-card add-space" @click="createSpace">
          <van-icon name="plus" size="32" />
          <p>创建新空间</p>
        </div>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="section stats-overview">
      <h3>资产统计</h3>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-value">{{ stats.totalItems }}</span>
          <span class="stat-label">物品总数</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ stats.totalValue }}</span>
          <span class="stat-label">总价值</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ stats.totalSpaces }}</span>
          <span class="stat-label">空间数</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ stats.thisMonth }}</span>
          <span class="stat-label">本月新增</span>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <van-tabbar v-model="activeTab" route>
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="apps-o" to="/spaces">空间</van-tabbar-item>
      <van-tabbar-item icon="scan" to="/scan" class="scan-tab">
        <template #icon>
          <div class="scan-button">
            <van-icon name="scan" size="24" />
          </div>
        </template>
      </van-tabbar-item>
      <van-tabbar-item icon="medal-o" to="/achievements">成就</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { showToast, showLoadingToast, closeToast } from 'vant';

const router = useRouter();
const activeTab = ref(0);
const searchKeyword = ref('');

// 最近添加的物品
const recentItems = ref([
  {
    id: 1,
    name: '索尼WH-1000XM4耳机',
    category: '电子产品',
    image: 'https://via.placeholder.com/200?text=Headphones',
    space: '卧室',
    price: '¥2,299'
  },
  {
    id: 2,
    name: '宜家POÄNG扶手椅',
    category: '家具',
    image: 'https://via.placeholder.com/200?text=Chair',
    space: '客厅',
    price: '¥599'
  },
  {
    id: 3,
    name: 'Kindle Paperwhite 5',
    category: '电子产品',
    image: 'https://via.placeholder.com/200?text=Kindle',
    space: '书房',
    price: '¥1,068'
  }
]);

// 空间列表
const spaces = ref([
  {
    id: 1,
    name: '客厅',
    itemCount: 23,
    cover: 'https://via.placeholder.com/400x300?text=Living+Room'
  },
  {
    id: 2,
    name: '卧室',
    itemCount: 15,
    cover: 'https://via.placeholder.com/400x300?text=Bedroom'
  },
  {
    id: 3,
    name: '书房',
    itemCount: 42,
    cover: 'https://via.placeholder.com/400x300?text=Study'
  }
]);

// 统计数据
const stats = reactive({
  totalItems: 156,
  totalValue: '¥128,560',
  totalSpaces: 5,
  thisMonth: 12
});

onMounted(() => {
  // 加载数据
  loadData();
});

const loadData = () => {
  showLoadingToast({
    message: '加载中...',
    forbidClick: true,
  });
  
  // 模拟API调用
  setTimeout(() => {
    closeToast();
  }, 500);
};

const onSearch = () => {
  if (!searchKeyword.value.trim()) {
    showToast('请输入搜索关键词');
    return;
  }
  router.push(`/search?q=${encodeURIComponent(searchKeyword.value)}`);
};

const goToScan = () => {
  router.push('/scan');
};

const goToAddItem = () => {
  router.push('/scan');
};

const goToItems = () => {
  router.push('/items');
};

const goToSpaces = () => {
  router.push('/spaces');
};

const goToStats = () => {
  showToast('统计功能开发中');
};

const viewItem = (item) => {
  router.push(`/item/${item.id}`);
};

const enterSpace = (space) => {
  router.push(`/space/${space.id}`);
};

const createSpace = () => {
  router.push('/spaces/create');
};
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: #f7f8fa;
  padding-bottom: 70px;
}

.search-header {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  background: white;
  gap: 10px;
}

.search-header .van-search {
  flex: 1;
  padding: 0;
}

.scan-icon {
  font-size: 24px;
  color: #1989fa;
  padding: 8px;
}

.quick-actions {
  background: white;
  padding: 15px 0;
  margin-bottom: 10px;
}

:deep(.quick-actions .van-grid-item__content) {
  padding: 16px 8px;
}

:deep(.quick-actions .van-grid-item__icon) {
  font-size: 28px;
  color: #1989fa;
}

:deep(.quick-actions .van-grid-item__text) {
  font-size: 12px;
  margin-top: 8px;
}

.section {
  background: white;
  margin-bottom: 10px;
  padding: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.items-list .van-card {
  background: #f7f8fa;
  margin-bottom: 10px;
  border-radius: 8px;
}

.items-list .van-card__thumb {
  border-radius: 4px;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 5px;
}

.item-location {
  font-size: 12px;
  color: #666;
}

.item-price {
  color: #ee0a24;
  font-weight: bold;
}

.spaces-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.space-card {
  position: relative;
  height: 120px;
  border-radius: 8px;
  background-size: cover;
  background-position: center;
  overflow: hidden;
}

.space-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  color: white;
}

.space-overlay h4 {
  font-size: 14px;
  margin-bottom: 3px;
}

.space-overlay p {
  font-size: 12px;
  opacity: 0.9;
}

.add-space {
  background: #f0f0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed #ccc;
}

.add-space p {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.stat-item {
  background: #f7f8fa;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #1989fa;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.scan-button {
  width: 40px;
  height: 40px;
  background: #1989fa;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-top: -10px;
}
</style>