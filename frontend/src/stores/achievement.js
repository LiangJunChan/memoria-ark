import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { get } from '@/utils/request'
import { showToast } from 'vant'

export const useAchievementStore = defineStore('achievement', () => {
  // State
  const totalAssets = ref(0)
  const totalCarbon = ref(0)
  const medals = ref([])
  const rank = ref(null)
  const categoryStats = ref([])
  const dailyStats = ref([])
  const loading = ref(false)

  // Getters
  const hasMedal = computed(() => (medalId) => {
    return medals.value.some(m => m.id === medalId)
  })

  const unlockedCount = computed(() => medals.value.length)

  const nextMilestone = computed(() => {
    const milestones = [
      { count: 1, name: '首次收藏' },
      { count: 10, name: '收藏达人' },
      { count: 50, name: '收藏大师' },
      { count: 100, name: '收藏传奇' }
    ]
    return milestones.find(m => m.count > totalAssets.value) || milestones[milestones.length - 1]
  })

  // Actions
  const fetchAchievementData = async () => {
    loading.value = true
    try {
      const res = await get('/achievement/data')
      if (res.code === 0) {
        const data = res.data
        totalAssets.value = data.total_assets || 0
        totalCarbon.value = data.total_carbon_reduction || 0
        medals.value = data.medals || []
        rank.value = data.rank
      }
    } catch (error) {
      console.error('获取成就数据失败:', error)
      showToast('获取成就数据失败')
    } finally {
      loading.value = false
    }
  }

  const fetchStatistics = async () => {
    try {
      const res = await get('/achievement/statistics')
      if (res.code === 0) {
        const data = res.data
        categoryStats.value = data.category_stats || []
        dailyStats.value = data.daily_stats || []
      }
    } catch (error) {
      console.error('获取统计数据失败:', error)
    }
  }

  const checkMedals = async () => {
    try {
      const res = await fetch('/achievement/check-medals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      }).then(r => r.json())
      
      if (res.code === 0 && res.data.new_medals.length > 0) {
        const newMedals = res.data.new_medals
        showToast({
          message: `恭喜获得 ${newMedals.length} 枚新勋章！`,
          duration: 3000
        })
        // 刷新成就数据
        await fetchAchievementData()
        return newMedals
      }
      return []
    } catch (error) {
      console.error('检查勋章失败:', error)
      return []
    }
  }

  const addAsset = async (assetData) => {
    // 本地更新数据
    totalAssets.value += 1
    totalCarbon.value += assetData.carbon_reduction || 0
    
    // 检查是否有新勋章
    await checkMedals()
  }

  return {
    // State
    totalAssets,
    totalCarbon,
    medals,
    rank,
    categoryStats,
    dailyStats,
    loading,
    // Getters
    hasMedal,
    unlockedCount,
    nextMilestone,
    // Actions
    fetchAchievementData,
    fetchStatistics,
    checkMedals,
    addAsset
  }
})
