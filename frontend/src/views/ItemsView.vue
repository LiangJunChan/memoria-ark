<template>
  <div class="items-view">
    <van-nav-bar title="物品列表" left-arrow @click-left="$router.back()" fixed>
      <template #right>
        <van-icon name="search" size="20" @click="showSearch = true" />
      </template>
    </van-nav-bar>

    <van-search
      v-model="searchKeyword"
      placeholder="搜索物品"
      :show="showSearch"
      @cancel="showSearch = false"
      @search="onSearch"
    />

    <div class="filter-bar">
      <van-dropdown-menu>
        <van-dropdown-item v-model="filter.category" :options="categoryOptions" />
        <van-dropdown-item v-model="filter.space" :options="spaceOptions" />
        <van-dropdown-item v-model="filter.sort" :options="sortOptions" />
      </van-dropdown-menu>
    </div>

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多物品了"
        @load="onLoad"
      >
        <van-card
          v-for="item in filteredItems"
          :key="item.id"
          :title="item.name"
          :desc="item.category + ' · ' + item.space"
          :thumb="item.image"
          @click="viewItem(item)"
        >
          <template #price>
            <span class="item-price">{{ item.price }}</span>
          </template>
          <template #tags>
            <van-tag size="small" type="primary">{{ item.status }}</van-tag>
          </template>
        </van-card>
      </van-list>
    </van-pull-refresh>

    <van-fab
      icon="plus"
      type="primary"
      position="bottom-right"
      @click="addItem"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';

const router = useRouter();
const loading = ref(false);
const finished = ref(false);
const refreshing = ref(false);
const showSearch = ref(false);
const searchKeyword = ref('');

const filter = reactive({
  category: '',
  space: '',
  sort: 'default'
});

const categoryOptions = [
  { text: '全部分类', value: '' },
  { text: '家具', value: 'furniture' },
  { text: '电子产品', value: 'electronics' },
  { text: '书籍', value: 'books' },
  { text: '衣物', value: 'clothing' }
];

const spaceOptions = [
  { text: '全部空间', value: '' },
  { text: '客厅', value: 'living' },
  { text: '卧室', value: 'bedroom' },
  { text: '书房', value: 'study' },
  { text: '厨房', value: 'kitchen' }
];

const sortOptions = [
  { text: '默认排序', value: 'default' },
  { text: '价格从高到低', value: 'price_desc' },
  { text: '价格从低到高', value: 'price_asc' },
  { text: '最新添加', value: 'time_desc' }
];

const items = ref([
  {
    id: 1,
    name: '索尼WH-1000XM4耳机',
    category: '电子产品',
    space: '卧室',
    price: '¥2,299',
    image: 'https://via.placeholder.com/100?text=1',
    status: '完好'
  },
  {
    id: 2,
    name: '宜家POÄNG扶手椅',
    category: '家具',
    space: '客厅',
    price: '¥599',
    image: 'https://via.placeholder.com/100?text=2',
    status: '完好'
  },
  {
    id: 3,
    name: 'Kindle Paperwhite 5',
    category: '电子产品',
    space: '书房',
    price: '¥1,068',
    image: 'https://via.placeholder.com/100?text=3',
    status: '完好'
  }
]);

const filteredItems = computed(() => {
  return items.value.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchKeyword.value.toLowerCase());
    const matchesCategory = !filter.category || item.category === filter.category;
    const matchesSpace = !filter.space || item.space === filter.space;
    return matchesSearch && matchesCategory && matchesSpace;
  });
});

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

const onSearch = () => {
  showToast(`搜索：${searchKeyword.value}`);
};

const viewItem = (item) => {
  router.push(`/item/${item.id}`);
};

const addItem = () => {
  router.push('/scan');
};
</script>

<style scoped>
.items-view { min-height: 100vh; background: #f7f8fa; }
.filter-bar { background: white; padding-top: 46px; }
.van-card { background: white; margin: 8px; border-radius: 8px; }
.item-price { color: #ee0a24; font-weight: bold; }
</style>
