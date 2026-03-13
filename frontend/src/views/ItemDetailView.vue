<template>
  <div class="item-detail">
    <van-nav-bar title="物品详情" left-arrow @click-left="$router.back()" fixed>
      <template #right>
        <van-icon name="ellipsis" size="20" @click="showActions = true" />
      </template>
    </van-nav-bar>

    <van-swipe :autoplay="3000" indicator-color="white">
      <van-swipe-item v-for="image in item.images" :key="image">
        <van-image :src="image" width="100%" height="300" fit="cover" />
      </van-swipe-item>
    </van-swipe>

    <div class="item-info">
      <h2 class="item-name">{{ item.name }}</h2>
      <div class="item-tags">
        <van-tag type="primary">{{ item.category }}</van-tag>
        <van-tag type="success">{{ item.space }}</van-tag>
        <van-tag type="warning">{{ item.status }}</van-tag>
      </div>
      <div class="item-price">
        <span class="price-label">购买价格</span>
        <span class="price-value">{{ item.price }}</span>
      </div>
    </div>

    <van-cell-group inset>
      <van-cell title="购买日期" :value="item.purchaseDate" />
      <van-cell title="购买渠道" :value="item.purchaseChannel" />
      <van-cell title="保修期" :value="item.warranty" />
      <van-cell title="当前位置" :value="item.location" />
      <van-cell title="最后使用" :value="item.lastUsed" />
    </van-cell-group>

    <div class="notes-section" v-if="item.notes">
      <h3>备注</h3>
      <p>{{ item.notes }}</p>
    </div>

    <div class="qrcode-section">
      <h3>物品二维码</h3>
      <van-image
        width="200"
        height="200"
        :src="item.qrcode"
        fit="cover"
      />
      <p>扫码查看物品详情</p>
    </div>

    <div class="action-buttons">
      <van-grid :column-num="3" :border="false">
        <van-grid-item icon="edit" text="编辑" @click="editItem" />
        <van-grid-item icon="location-o" text="转移位置" @click="moveItem" />
        <van-grid-item icon="delete-o" text="删除" @click="deleteItem" />
      </van-grid>
    </div>

    <van-action-sheet
      v-model:show="showActions"
      :actions="actions"
      cancel-text="取消"
      close-on-click-action
      @select="onActionSelect"
    />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { showToast, showConfirmDialog } from 'vant';

const router = useRouter();
const route = useRoute();
const showActions = ref(false);

const item = reactive({
  id: route.params.id,
  name: '索尼WH-1000XM4耳机',
  category: '电子产品',
  space: '卧室',
  status: '完好',
  price: '¥2,299',
  images: [
    'https://via.placeholder.com/400x300?text=1',
    'https://via.placeholder.com/400x300?text=2',
    'https://via.placeholder.com/400x300?text=3'
  ],
  purchaseDate: '2024-01-15',
  purchaseChannel: '京东自营',
  warranty: '2026-01-14',
  location: '卧室床头柜',
  lastUsed: '2024-03-12',
  notes: '非常好用的降噪耳机，每天都用。',
  qrcode: 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://memoria-ark.com/item/1'
});

const actions = [
  { name: '编辑物品', value: 'edit' },
  { name: '转移位置', value: 'move' },
  { name: '生成二维码', value: 'qrcode' },
  { name: '添加维护记录', value: 'maintenance' },
  { name: '导出信息', value: 'export' },
  { name: '删除物品', value: 'delete', color: '#ee0a24' }
];

const onActionSelect = (action) => {
  switch (action.value) {
    case 'edit': editItem(); break;
    case 'move': moveItem(); break;
    case 'qrcode': generateQrcode(); break;
    case 'maintenance': addMaintenance(); break;
    case 'export': exportItem(); break;
    case 'delete': deleteItem(); break;
  }
};

const editItem = () => {
  showToast('编辑功能开发中');
};

const moveItem = () => {
  showToast('转移位置功能开发中');
};

const deleteItem = async () => {
  try {
    await showConfirmDialog({
      title: '确认删除',
      message: '确定要删除这个物品吗？删除后无法恢复。'
    });
    showToast('删除成功');
    router.back();
  } catch (error) {
    // 用户取消
  }
};

const generateQrcode = () => {
  showToast('二维码已生成');
};

const addMaintenance = () => {
  showToast('添加维护记录功能开发中');
};

const exportItem = () => {
  showToast('导出功能开发中');
};
</script>

<style scoped>
.item-detail { min-height: 100vh; background: #f7f8fa; padding-bottom: 20px; }
.item-info { background: white; padding: 16px; margin-bottom: 10px; }
.item-name { font-size: 20px; font-weight: bold; margin-bottom: 12px; }
.item-tags { margin-bottom: 12px; }
.item-tags .van-tag { margin-right: 8px; }
.item-price { display: flex; justify-content: space-between; align-items: center; }
.price-value { font-size: 24px; color: #ee0a24; font-weight: bold; }
.notes-section { background: white; padding: 16px; margin-bottom: 10px; }
.notes-section h3 { font-size: 16px; margin-bottom: 8px; }
.notes-section p { color: #666; line-height: 1.5; }
.qrcode-section { background: white; padding: 16px; margin-bottom: 10px; text-align: center; }
.qrcode-section h3 { font-size: 16px; margin-bottom: 12px; }
.qrcode-section p { color: #666; margin-top: 8px; }
.action-buttons { margin: 0 10px; background: white; border-radius: 8px; }
</style>
