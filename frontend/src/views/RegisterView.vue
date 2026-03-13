<template>
  <div class="register-view">
    <van-nav-bar title="注册账号" left-arrow @click-left="$router.back()" />
    <div class="register-form">
      <van-form @submit="onSubmit">
        <van-field v-model="form.username" name="username" label="用户名" placeholder="请输入用户名" :rules="[{ required: true }]" />
        <van-field v-model="form.email" name="email" label="邮箱" placeholder="请输入邮箱" :rules="[{ required: true }]" />
        <van-field v-model="form.phone" name="phone" label="手机号" placeholder="请输入手机号" />
        <van-field v-model="form.password" type="password" name="password" label="密码" placeholder="请输入密码" :rules="[{ required: true }]" />
        <van-field v-model="form.confirmPassword" type="password" name="confirmPassword" label="确认密码" placeholder="请再次输入密码" :rules="[{ required: true, validator: validateConfirmPassword }]" />
        <div style="margin: 16px;">
          <van-button round block type="primary" native-type="submit" :loading="loading">注册</van-button>
        </div>
      </van-form>
      <div class="login-link">
        已有账号？<a @click="goToLogin">立即登录</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { showToast, showLoadingToast, closeToast } from 'vant';

const router = useRouter();
const loading = ref(false);

const form = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
});

const validateConfirmPassword = (value) => {
  if (value !== form.password) {
    return '两次输入的密码不一致';
  }
  return true;
};

const onSubmit = async () => {
  loading.value = true;
  showLoadingToast({ message: '注册中...', forbidClick: true });

  try {
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    closeToast();
    showToast('注册成功');
    router.push('/login');
  } catch (error) {
    closeToast();
    showToast(error.message || '注册失败');
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.register-view { min-height: 100vh; background: #f7f8fa; }
.register-form { padding: 20px; }
.login-link { text-align: center; margin-top: 20px; color: #666; }
.login-link a { color: #1989fa; cursor: pointer; }
</style>