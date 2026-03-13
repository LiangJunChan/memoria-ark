<template>
  <div class="space-roaming">
    <van-nav-bar
      title="3D空间漫游"
      left-arrow
      @click-left="$router.back()"
    />
    
    <div class="space-info">
      <van-cell-group>
        <van-cell title="当前空间" :value="currentSpace.name" />
        <van-cell title="物品数量" :value="itemCount + '件'" />
      </van-cell-group>
    </div>

    <div class="roaming-container">
      <canvas ref="canvasRef" class="roaming-canvas"></canvas>
      
      <div class="roaming-controls">
        <van-button 
          round 
          type="primary" 
          size="small"
          @click="enterVRMode"
        >
          VR模式
        </van-button>
        <van-button 
          round 
          type="info" 
          size="small"
          @click="toggleFullscreen"
        >
          全屏
        </van-button>
      </div>

      <div class="item-markers">
        <div 
          v-for="item in visibleItems" 
          :key="item.id"
          class="item-marker"
          :style="{ left: item.x + '%', top: item.y + '%' }"
          @click="selectItem(item)"
        >
          <van-icon name="point-gift" />
          <span class="marker-label">{{ item.name }}</span>
        </div>
      </div>
    </div>

    <van-action-sheet
      v-model:show="showItemDetail"
      :title="selectedItem?.name"
    >
      <div class="item-detail">
        <van-image
          width="100%"
          height="200"
          fit="cover"
          :src="selectedItem?.image"
        />
        <van-cell-group>
          <van-cell title="类别" :value="selectedItem?.category" />
          <van-cell title="购买日期" :value="selectedItem?.purchaseDate" />
          <van-cell title="价格" :value="selectedItem?.price" />
          <van-cell title="位置" :value="selectedItem?.location" />
        </van-cell-group>
        <van-cell title="备注" :label="selectedItem?.notes" />
        <div class="detail-actions">
          <van-button type="primary" block @click="editItem">编辑</van-button>
          <van-button type="danger" block style="margin-top: 10px" @click="deleteItem">删除</van-button>
        </div>
      </div>
    </van-action-sheet>

    <van-tabbar v-model="activeTab" route>
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="apps-o" to="/spaces">空间</van-tabbar-item>
      <van-tabbar-item icon="scan" to="/scan">扫描</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const canvasRef = ref(null);
const activeTab = ref(1);
const showItemDetail = ref(false);
const selectedItem = ref(null);

// 当前空间信息
const currentSpace = ref({
  id: 1,
  name: '客厅',
  description: '主要活动区域'
});

// 物品列表
const items = ref([
  { id: 1, name: '沙发', x: 20, y: 30, category: '家具', price: '¥3,999', image: 'https://via.placeholder.com/400x300?text=Sofa' },
  { id: 2, name: '电视柜', x: 50, y: 40, category: '家具', price: '¥1,299', image: 'https://via.placeholder.com/400x300?text=TV+Stand' },
  { id: 3, name: '茶几', x: 35, y: 60, category: '家具', price: '¥899', image: 'https://via.placeholder.com/400x300?text=Tea+Table' },
]);

const itemCount = computed(() => items.value.length);
const visibleItems = computed(() => items.value);

// 3D场景初始化
onMounted(() => {
  init3DScene();
});

const init3DScene = () => {
  const canvas = canvasRef.value;
  if (!canvas) return;
  
  // 设置canvas尺寸
  const container = canvas.parentElement;
  canvas.width = container.clientWidth;
  canvas.height = container.clientHeight;
  
  // 获取2D上下文
  const ctx = canvas.getContext('2d');
  
  // 绘制3D房间轮廓
  draw3DRoom(ctx, canvas.width, canvas.height);
};

const draw3DRoom = (ctx, width, height) => {
  // 清空画布
  ctx.clearRect(0, 0, width, height);
  
  // 绘制地板
  ctx.fillStyle = '#f0f0f0';
  ctx.fillRect(50, height/2, width-100, height/2-50);
  
  // 绘制墙壁
  ctx.fillStyle = '#e0e0e0';
  ctx.fillRect(50, 50, width-100, height/2-50);
  
  // 绘制透视线条
  ctx.strokeStyle = '#ccc';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(50, height/2);
  ctx.lineTo(100, height-100);
  ctx.moveTo(width-50, height/2);
  ctx.lineTo(width-100, height-100);
  ctx.stroke();
  
  // 绘制提示文字
  ctx.fillStyle = '#999';
  ctx.font = '14px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('3D空间漫游视图', width/2, 30);
  ctx.fillText('（点击物品标记查看详情）', width/2, height-20);
};

// VR模式
const enterVRMode = () => {
  showToast('VR模式开发中，敬请期待');
};

// 全屏切换
const toggleFullscreen = () => {
  const elem = document.querySelector('.roaming-container');
  if (!document.fullscreenElement) {
    elem.requestFullscreen().catch(err => {
      showToast(`全屏模式错误: ${err.message}`);
    });
  } else {
    document.exitFullscreen();
  }
};

// 选择物品
const selectItem = (item) => {
  selectedItem.value = item;
  showItemDetail.value = true;
};

// 编辑物品
const editItem = () => {
  showToast('跳转到编辑页面');
  showItemDetail.value = false;
};

// 删除物品
const deleteItem = () => {
  showConfirmDialog({
    title: '确认删除',
    message: '确定要删除这个物品吗？'
  }).then(() => {
    items.value = items.value.filter(i => i.id !== selectedItem.value.id);
    showItemDetail.value = false;
    showToast('删除成功');
  }).catch(() => {});
};

// Toast提示
const showToast = (message) => {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed; top: 50%; left: 50%; 
    transform: translate(-50%, -50%);
    background: rgba(0,0,0,0.7); color: white;
    padding: 12px 24px; border-radius: 8px;
    z-index: 9999; font-size: 14px;
  `;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2000);
};

// 确认对话框
const showConfirmDialog = ({ title, message }) => {
  return new Promise((resolve, reject) => {
    const mask = document.createElement('div');
    mask.style.cssText = `
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.5); z-index: 10000;
      display: flex; align-items: center; justify-content: center;
    `;
    
    const dialog = document.createElement('div');
    dialog.style.cssText = `
      background: white; border-radius: 12px;
      width: 280px; padding: 20px;
    `;
    dialog.innerHTML = `
      <h3 style="margin: 0 0 10px; font-size: 16px;">${title}</h3>
      <p style="margin: 0 0 20px; color: #666; font-size: 14px;">${message}</p>
      <div style="display: flex; gap: 10px;">
        <button class="cancel-btn" style="flex: 1; padding: 8px; border: 1px solid #ddd; background: white; border-radius: 4px;">取消</button>
        <button class="confirm-btn" style="flex: 1; padding: 8px; border: none; background: #1989fa; color: white; border-radius: 4px;">确定</button>
      </div>
    `;
    
    mask.appendChild(dialog);
    document.body.appendChild(mask);
    
    dialog.querySelector('.cancel-btn').onclick = () => {
      mask.remove();
      reject();
    };
    dialog.querySelector('.confirm-btn').onclick = () => {
      mask.remove();
      resolve();
    };
  });
};
</script>

<style scoped>
.space-roaming {
  min-height: 100vh;
  background: #f7f8fa;
  padding-bottom: 60px;
}

.space-info {
  margin: 12px;
}

.roaming-container {
  position: relative;
  margin: 12px;
  height: 400px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.roaming-canvas {
  width: 100%;
  height: 100%;
}

.roaming-controls {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
}

.item-markers {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.item-marker {
  position: absolute;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  pointer-events: auto;
  padding: 4px 8px;
  background: rgba(25, 137, 250, 0.9);
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.item-marker .van-icon {
  font-size: 20px;
  color: white;
}

.marker-label {
  font-size: 12px;
  color: white;
  margin-top: 2px;
  white-space: nowrap;
}

.item-detail {
  padding: 16px;
}

.detail-actions {
  margin-top: 20px;
}
</style>