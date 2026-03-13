<template>
  <div class="profile-view">
    <van-nav-bar title="我的" fixed />

    <div class="profile-header">
      <van-image round width="80" height="80" :src="user.avatar" />
      <h3>{{ user.nickname }}</h3>
      <p>{{ user.username }}</p>
      <van-tag type="primary" size="medium">{{ user.level }}</van-tag>
    </div>

    <van-cell-group inset class="stats-group">
      <van-row>
        <van-col span="8" class="stat-col">
          <div class="stat-value">{{ stats.items }}</div>
          <div class="stat-label">物品</div>
        </van-col>
        <van-col span="8" class="stat-col">
          <div class="stat-value">{{ stats.spaces }}</div>
          <div class="stat-label">空间</div>
        </van-col>
        <van-col span="8" class="stat-col">
          <div class="stat-value">{{ stats.achievements }}</div>
          <div class="stat-label">成就</div>
        </van-col>
      </van-row>
    </van-cell-group>

    <van-cell-group inset>
      <van-cell title="编辑资料" icon="edit" is-link @click="editProfile" />
      <van-cell title="我的收藏" icon="star-o" is-link />
      <van-cell title="浏览历史" icon="clock-o" is-link />
    </van-cell-group>

    <van-cell-group inset style="margin-top: 10px;">
      <van-cell title="账号安全" icon="shield-o" is-link />
      <van-cell title="通知设置" icon="bell-o" is-link />
      <van-cell title="隐私设置" icon="eye-o" is-link />
    </van-cell-group>

    <van-cell-group inset style="margin-top: 10px;">
      <van-cell title="帮助与反馈" icon="question-o" is-link />
      <van-cell title="关于我们" icon="info-o" is-link />
    </van-cell-group>

    <div style="margin: 20px;">
      <van-button round block type="danger" plain @click="logout">退出登录</van-button>
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
import { useUserStore } from '@/stores/user';
import { showToast, showConfirmDialog } from 'vant';

const router = useRouter();
const userStore = useUserStore();
const activeTab = ref(4);

const user = ref({
  avatar: 'https://via.placeholder.com/100?text=Avatar',
  nickname: '数字收藏家',
  username: 'user123',
  level: '资深收藏家'
});

const stats = ref({
  items: 156,
  spaces: 8,
  achievements: 23
});

const editProfile = () => {
  showToast('编辑资料功能开发中');
};

const logout = async () => {
  try {
    await showConfirmDialog({
      title: '确认退出',
      message: '确定要退出登录吗？'
    });
    await userStore.logout();
    showToast('已退出登录');
    router.push('/login');
  } catch (error) {
    // 用户取消
  }
};
</script>

<style scoped>
.profile-view { min-height: 100vh; background: #f7f8fa; padding-bottom: 70px; }
.profile-header { text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.profile-header h3 { font-size: 20px; margin: 15px 0 5px; }
.profile-header p { opacity: 0.8; margin-bottom: 10px; }
.stats-group { margin: -30px 16px 10px; position: relative; z-index: 1; background: white; border-radius: 12px; padding: 20px 0; text-align: center; }
.stat-col { border-right: 1px solid #f0f0f0; }
.stat-col:last-child { border-right: none; }
.stat-value { font-size: 24px; font-weight: bold; color: #333; }
.stat-label { font-size: 12px; color: #999; margin-top: 5px; }
</style>
