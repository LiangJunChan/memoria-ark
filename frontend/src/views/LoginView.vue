<template>
  <div class="login-view">
    <div class="login-header">
      <van-image
        width="120"
        height="120"
        src="/logo.png"
        fit="contain"
      />
      <h1>忆存·数字方舟</h1>
      <p>记录生活的每一个珍贵时刻</p>
    </div>

    <van-form class="login-form" @submit="onSubmit">
      <van-field
        v-model="form.username"
        name="username"
        placeholder="用户名/邮箱/手机号"
        :rules="[{ required: true, message: '请填写用户名' }]"
      >
        <template #left-icon>
          <van-icon name="user-o" />
        </template>
      </van-field>

      <van-field
        v-model="form.password"
        type="password"
        name="password"
        placeholder="密码"
        :rules="[{ required: true, message: '请填写密码' }]"
      >
        <template #left-icon>
          <van-icon name="lock" />
        </template>
      </van-field>

      <div class="form-options">
        <van-checkbox v-model="rememberMe" shape="square">记住我</van-checkbox>
        <a href="#" @click.prevent="forgotPassword">忘记密码？</a>
      </div>

      <div class="form-actions">
        <van-button round block type="primary" native-type="submit" :loading="loading">
          登录
        </van-button>
        <van-button round block plain type="primary" style="margin-top: 12px;" @click="goToRegister">
          注册账号
        </van-button>
      </div>
    </van-form>

    <div class="third-party-login">
      <van-divider>其他登录方式</van-divider>
      <div class="third-party-icons">
        <van-button icon="wechat" round plain type="success" size="large" />
        <van-button icon="alipay" round plain type="primary" size="large" />
        <van-button icon="phone-circle-o" round plain type="warning" size="large" />
      </div>
    </div>

    <p class="copyright">© 2024 忆存·数字方舟</p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { showToast, showLoadingToast, closeToast } from 'vant';

const router = useRouter();
const userStore = useUserStore();
const loading = ref(false);
const rememberMe = ref(false);

const form = reactive({
  username: '',
  password: ''
});

const onSubmit = async () => {
  loading.value = true;
  showLoadingToast({
    message: '登录中...',
    forbidClick: true,
  });

  try {
    // 模拟登录API调用
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // 模拟登录成功
    const mockUser = {
      id: 1,
      username: form.username,
      nickname: '用户' + form.username,
      avatar: 'https://via.placeholder.com/100?text=Avatar',
      token: 'mock_token_' + Date.now()
    };

    userStore.setUser(mockUser);
    closeToast();
    showToast('登录成功');
    
    // 跳转到首页
    router.push('/');
  } catch (error) {
    closeToast();
    showToast(error.message || '登录失败');
  } finally {
    loading.value = false;
  }
};

const goToRegister = () => {
  router.push('/register');
};

const forgotPassword = () => {
  showToast('请联系客服重置密码');
};
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  box-sizing: border-box;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
  color: white;
}

.login-header h1 {
  font-size: 24px;
  margin: 15px 0 5px;
}

.login-header p {
  font-size: 14px;
  opacity: 0.9;
}

.login-form {
  width: 100%;
  max-width: 320px;
  background: white;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

:deep(.van-field) {
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 12px;
}

:deep(.van-field__left-icon) {
  margin-right: 8px;
  color: #666;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 15px 0;
  font-size: 13px;
}

.form-options a {
  color: #667eea;
  text-decoration: none;
}

.form-actions {
  margin-top: 20px;
}

:deep(.van-button--round) {
  border-radius: 24px;
}

.third-party-login {
  width: 100%;
  max-width: 320px;
  margin-top: 30px;
  text-align: center;
}

.third-party-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 15px;
}

.third-party-icons .van-button {
  width: 50px;
  height: 50px;
  padding: 0;
}

.copyright {
  margin-top: 30px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
}

:deep(.van-divider) {
  color: rgba(255, 255, 255, 0.8);
  border-color: rgba(255, 255, 255, 0.3);
}

:deep(.van-divider::before),
:deep(.van-divider::after) {
  border-color: rgba(255, 255, 255, 0.3);
}
</style>