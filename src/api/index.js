import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 创建账号分发链接
export const createLink = async (accounts, expireHours, oneTime = false, allowDestroy = false, viewPassword = '') => {
  try {
    const response = await api.post('/api/create', {
      accounts,
      expire_hours: expireHours,
      one_time: oneTime,
      allow_destroy: allowDestroy,
      view_password: viewPassword,
    });
    return response.data;
  } catch (error) {
    console.error('创建链接失败:', error);
    throw error.response?.data || { error: '创建链接失败' };
  }
};

// 获取链接内容
export const getLink = async (uuid, password = '') => {
  try {
    const response = await api.get(`/api/link/${uuid}`, {
      params: { password }
    });
    return response.data;
  } catch (error) {
    console.error('获取链接失败:', error);
    throw error.response?.data || { error: '获取链接失败' };
  }
};

// 检查链接状态
export const checkStatus = async (uuid) => {
  try {
    const response = await api.get(`/api/status/${uuid}`);
    return response.data;
  } catch (error) {
    console.error('检查状态失败:', error);
    throw error.response?.data || { error: '检查状态失败' };
  }
};

// 使链接失效
export const deactivateLink = async (uuid) => {
  try {
    const response = await api.delete(`/api/link/${uuid}`);
    return response.data;
  } catch (error) {
    console.error('失效链接失败:', error);
    throw error.response?.data || { error: '失效链接失败' };
  }
};

export default api;