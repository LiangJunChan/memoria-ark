import axios from 'axios';
import { showToast, showDialog } from 'vant';

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  withCredentials: true,
});

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    
    config.headers['Content-Type'] = config.headers['Content-Type'] || 'application/json';
    
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  error => {
    console.error('request error:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data;
    
    if (res.code === 200 || res.status === 200) {
      return res;
    } else if (res.code === 401) {
      showDialog({
        title: '提示',
        message: '登录已过期，请重新登录',
      }).then(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      });
      return Promise.reject(new Error(res.message || '未授权'));
    } else {
      showToast(res.message || '请求失败');
      return Promise.reject(new Error(res.message || '请求失败'));
    }
  },
  error => {
    console.error('response error:', error);
    const status = error.response?.status;
    
    if (status === 401) {
      showDialog({
        title: '提示',
        message: '登录已过期，请重新登录',
      }).then(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      });
    } else {
      showToast('网络异常，请稍后重试');
    }
    
    return Promise.reject(error);
  }
);

export default service;

// 简化的HTTP方法
export const get = (url, params) => service.get(url, { params });
export const post = (url, data) => service.post(url, data);
export const put = (url, data) => service.put(url, data);
export const del = (url) => service.delete(url);
