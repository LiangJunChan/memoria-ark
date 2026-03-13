import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const currentUser = computed(() => user.value)
  const userId = computed(() => user.value?.id)
  const username = computed(() => user.value?.username)
  const nickname = computed(() => user.value?.nickname || user.value?.username)
  const avatar = computed(() => user.value?.avatar || '/default-avatar.png')

  // Actions
  const initUser = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (e) {
        console.error('Failed to parse user data:', e)
        localStorage.removeItem('user')
      }
    }
  }

  const setUser = (userData) => {
    user.value = userData
    token.value = userData.token
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('token', userData.token)
  }

  const updateUser = (userData) => {
    user.value = { ...user.value, ...userData }
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  const updateAvatar = (avatarUrl) => {
    if (user.value) {
      user.value.avatar = avatarUrl
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  const clearUser = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  const logout = async () => {
    loading.value = true
    try {
      // 可以在这里调用登出API
      // await api.post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      clearUser()
      loading.value = false
    }
  }

  const fetchUserProfile = async () => {
    try {
      // 调用获取用户资料API
      // const response = await api.get('/user/profile')
      // updateUser(response.data)
    } catch (error) {
      console.error('Fetch user profile error:', error)
    }
  }

  return {
    // State
    user,
    token,
    loading,
    // Getters
    isAuthenticated,
    currentUser,
    userId,
    username,
    nickname,
    avatar,
    // Actions
    initUser,
    setUser,
    updateUser,
    updateAvatar,
    clearUser,
    logout,
    fetchUserProfile
  }
})