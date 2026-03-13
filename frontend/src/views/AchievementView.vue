<template>
  <div class="achievement-view">
    <!-- 顶部统计卡片 -->
    <div class="stats-card">
      <div class="stat-item">
        <div class="stat-number">{{ achievementStore.totalAssets }}</div>
        <div class="stat-label">数字藏品</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-number">{{ achievementStore.totalCarbon.toFixed(1) }}</div>
        <div class="stat-label">减碳(kg)</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-number">{{ achievementStore.medals.length }}</div>
        <div class="stat-label">获得勋章</div>
      </div>
    </div>

    <!-- 勋章展示区域 -->
    <div class="section-title">
      <span>我的勋章</span>
      <span class="sub-title">共 {{ achievementStore.medals.length }} 枚</span>
    </div>
    
    <div class="medals-grid">
      <div 
        v-for="medal in achievementStore.medals" 
        :key="medal.id"
        class="medal-card"
        @click="showMedalDetail(medal)"
      >
        <div class="medal-icon">{{ medal.icon || '🏆' }}</div>
        <div class="medal-name">{{ medal.name }}</div>
        <div class="medal-time">{{ formatTime(medal.unlock_time) }}</div>
      </div>
      
      <!-- 未解锁勋章占位 -->
      <div 
        v-for="n in (6 - achievementStore.medals.length)" 
        :key="`locked-${n}`"
        class="medal-card locked"
      >
        <div class="medal-icon">🔒</div>
        <div class="medal-name">未解锁</div>
        <div class="medal-time">继续努力</div>
      </div>
    </div>

    <!-- 排行榜入口 -->
    <div class="ranking-entry" @click="goToRanking">
      <div class="ranking-info">
        <div class="ranking-title">🏆 环保贡献排行榜</div>
        <div class="ranking-desc">查看你的环保排名</div>
      </div>
      <van-icon name="arrow" class="ranking-arrow" />
    </div>

    <!-- 环保小贴士 -->
    <div class="eco-tips">
      <div class="tips-title">💡 环保小贴士</div>
      <div class="tips-content">{{ currentTip }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAchievementStore } from '@/stores/achievement'
import { showToast } from 'vant'

const router = useRouter()
const achievementStore = useAchievementStore()

// 环保小贴士
const tips = [
  '每回收1件电子产品，可减少约5kg碳排放',
  '书籍回收再利用，可以拯救一片森林',
  '旧衣物回收比直接丢弃减少90%的碳排放',
  '定期整理家中物品，减少不必要的购买',
  '将闲置物品数字化保存，既环保又有意义'
]

const currentTip = computed(() => {
  const dayOfYear = Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24))
  return tips[dayOfYear % tips.length]
})

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

// 显示勋章详情
const showMedalDetail = (medal) => {
  showToast({
    message: `${medal.name}\n${medal.condition || '恭喜获得此勋章！'}`,
    duration: 2000
  })
}

// 跳转到排行榜
const goToRanking = () => {
  router.push('/ranking')
}

onMounted(() => {
  // 加载成就数据
  achievementStore.fetchAchievementData()
})
</script>

<style scoped>
.achievement-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 16px;
  padding-bottom: 80px;
}

/* 统计卡片 */
.stats-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: #eee;
}

/* 勋章区域 */
.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: bold;
}

.sub-title {
  font-size: 14px;
  font-weight: normal;
  opacity: 0.8;
}

.medals-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.medal-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 16px 8px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.medal-card:active {
  transform: scale(0.95);
}

.medal-card.locked {
  opacity: 0.6;
  background: rgba(255, 255, 255, 0.7);
}

.medal-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.medal-name {
  font-size: 12px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.medal-time {
  font-size: 10px;
  color: #999;
}

/* 排行榜入口 */
.ranking-entry {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.ranking-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.ranking-desc {
  font-size: 12px;
  color: #666;
}

.ranking-arrow {
  font-size: 20px;
  color: #999;
}

/* 环保小贴士 */
.eco-tips {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.tips-title {
  font-size: 14px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.tips-content {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}
</style>
