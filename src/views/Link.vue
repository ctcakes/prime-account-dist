<template>
  <div class="link-page">
    <div class="container">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <a-spin size="large" />
        <p class="loading-text">加载中...</p>
      </div>

      <!-- 链接过期或无效 -->
      <div v-else-if="!needPassword && (!linkData || linkData.status === 'expired')" class="expired-container">
        <a-card class="expired-card">
          <div class="expired-icon">
            <WarningOutlined />
          </div>
          <h1 class="expired-title">链接已失效</h1>
          <p class="expired-message">
            {{ linkData?.message || '此链接不存在或已过期' }}
          </p>
        </a-card>
      </div>

      <!-- 账号展示 -->
      <div v-else class="accounts-container">
        <!-- 密码输入界面 -->
        <div v-if="needPassword" class="password-container">
          <a-card class="password-card">
            <div class="password-card-header">
              <h2 class="password-title">请输入查看密码</h2>
            </div>
            <a-form layout="vertical" @submit.prevent="handlePasswordSubmit">
              <a-form-item>
                <a-input
                  v-model:value="passwordInput"
                  placeholder="请输入密码"
                  :type="showPasswordInput ? 'text' : 'password'"
                  size="large"
                  class="password-input-field"
                >
                  <template #suffix>
                    <a-button
                      type="text"
                      size="small"
                      @click="showPasswordInput = !showPasswordInput"
                    >
                      <EyeOutlined v-if="showPasswordInput" />
                      <EyeInvisibleOutlined v-else />
                    </a-button>
                  </template>
                </a-input>
              </a-form-item>
              <a-form-item>
                <a-button
                  type="primary"
                  size="large"
                  block
                  :loading="passwordLoading"
                  @click="handlePasswordSubmit"
                >
                  确认
                </a-button>
              </a-form-item>
              <div v-if="passwordError" class="password-error">
                <a-alert type="error" :message="passwordError" show-icon />
              </div>
            </a-form>
          </a-card>
        </div>

        <!-- 账号内容 -->
        <a-card v-else class="accounts-card">
          <!-- 已销毁提示 -->
          <a-alert
            v-if="isDestroyed"
            type="error"
            show-icon
            message="链接已销毁"
            description="此链接已被销毁，刷新页面后将无法再访问。请立即点击下方按钮保存或复制账号信息。"
            class="destroyed-alert"
          />

          <div class="card-header">
            <h1 class="title">内容信息</h1>
            <div class="header-actions">
              <a-tag color="green">
                链接失效：{{ linkData.remaining_hours }} 小时
              </a-tag>
            </div>
          </div>

          <a-alert
            v-if="linkData.one_time && !isDestroyed"
            type="warning"
            show-icon
            message="一次性链接警告"
            description="此链接为一次性链接，查看后将立即失效。请立即保存或复制内容！"
            class="one-time-alert"
          />

          <a-divider />

          <!-- 内容显示 -->
          <div class="content-display">
            <pre>{{ linkData.content }}</pre>
          </div>

          <a-divider />

          <!-- 操作按钮 -->
          <div class="actions">
            <a-button
              type="primary"
              size="large"
              @click="handleCopyAll"
              class="action-btn"
            >
              复制全部
            </a-button>
            <a-button
              size="large"
              @click="handleDownload"
              class="action-btn"
            >
              下载为TXT
            </a-button>
            <a-button
              v-if="linkData.allow_destroy && !isDestroyed"
              danger
              size="large"
              @click="handleDestroy"
              class="action-btn destroy-btn"
            >
              销毁链接
            </a-button>
          </div>
        </a-card>

        <!-- 安全提示 -->
        <a-alert
          type="info"
          show-icon
          class="security-alert"
        >
          <template #message>
            <span>安全提示</span>
          </template>
          <template #description>
            <div class="alert-content">
              <p>• 本项目完全开源，代码可审计</p>
              <p>• 不会窃取或保存账号数据</p>
              <p>• 请妥善保管账号信息，使用后建议及时修改密码</p>
            </div>
          </template>
        </a-alert>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { message, Modal } from 'ant-design-vue';
import { CopyOutlined, WarningOutlined, EyeInvisibleOutlined, EyeOutlined } from '@ant-design/icons-vue';
import { getLink, deactivateLink } from '../api';
import { copyToClipboard, downloadAsTxt, formatAccountsText } from '../utils/format';

const route = useRoute();
const router = useRouter();

const loading = ref(true);
const linkData = ref(null);
const needPassword = ref(false);
const passwordInput = ref('');
const showPasswordInput = ref(false);
const passwordLoading = ref(false);
const passwordError = ref('');
const isDestroyed = ref(false);

const fetchLinkData = async () => {
  const uuid = route.params.uuid;
  if (!uuid) {
    router.push('/');
    return;
  }

  loading.value = true;

  try {
    // 检查URL中是否有密码参数
    const urlParams = new URLSearchParams(window.location.search);
    const urlPassword = urlParams.get('pwd') || '';

    const data = await getLink(uuid, urlPassword);

    if (data.status === 'password_required') {
      needPassword.value = true;
      linkData.value = null;
    } else if (data.status === 'password_error') {
      needPassword.value = true;
      passwordError.value = '密码错误';
      linkData.value = null;
    } else if (data.status === 'active') {
      needPassword.value = false;
      linkData.value = data;
    } else {
      needPassword.value = false;
      linkData.value = data;
    }
  } catch (error) {
    message.error(error.error || '获取链接失败');
    linkData.value = null;
  } finally {
    loading.value = false;
  }
};

const copyText = async (text) => {
  const success = await copyToClipboard(text);
  if (success) {
    message.success('已复制到剪贴板');
  } else {
    message.error('复制失败');
  }
};

const handleCopyAll = async () => {
  const text = linkData.value.content;
  const success = await copyToClipboard(text);
  if (success) {
    message.success('已复制全部内容');
  } else {
    message.error('复制失败');
  }
};

const handleDownload = () => {
  downloadAsTxt([{ username: linkData.value.content, password: '' }], 'content.txt');
  message.success('下载已开始');
};

const handleDestroy = () => {
  Modal.confirm({
    title: '确认销毁链接？',
    content: '销毁后，此链接将立即失效，无法再次访问。请确认您已经保存了所有账号信息。',
    okText: '确认销毁',
    cancelText: '取消',
    okType: 'danger',
    onOk: async () => {
      const uuid = route.params.uuid;
      try {
        await deactivateLink(uuid);
        message.success('链接已销毁');
        isDestroyed.value = true;
      } catch (error) {
        message.error(error.error || '销毁链接失败');
      }
    }
  });
};

const handlePasswordSubmit = async () => {
  const uuid = route.params.uuid;
  passwordError.value = '';
  passwordLoading.value = true;

  try {
    const data = await getLink(uuid, passwordInput.value);

    if (data.status === 'password_required') {
      passwordError.value = '需要输入密码';
    } else if (data.status === 'password_error') {
      passwordError.value = '密码错误';
    } else if (data.status === 'active') {
      needPassword.value = false;
      linkData.value = data;
      message.success('密码验证成功');
    }
  } catch (error) {
    passwordError.value = error.error || '验证失败';
  } finally {
    passwordLoading.value = false;
  }
};

const goHome = () => {
  router.push('/');
};

onMounted(() => {
  fetchLinkData();
});
</script>

<style scoped>
.link-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 60px 24px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.container {
  max-width: 800px;
  width: 100%;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
}

.loading-text {
  margin-top: 20px;
  color: #666666;
  font-size: 16px;
}

/* 密码输入界面 */
.password-container {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.password-card {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
}

.password-card-header {
  text-align: center;
  margin-bottom: 24px;
}

.password-title {
  font-size: 24px;
  font-weight: 600;
  color: #333333;
  margin: 0;
}

.password-input-field {
  font-size: 16px;
}

.password-error {
  margin-top: 16px;
}

/* 过期状态 */
.expired-container {
  width: 100%;
}

.expired-card {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  text-align: center;
  padding: 60px 40px;
}

.expired-icon {
  font-size: 64px;
  margin-bottom: 24px;
  color: #ff4d4f;
}

.expired-title {
  font-size: 28px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 16px;
}

.expired-message {
  font-size: 16px;
  color: #666666;
  margin-bottom: 32px;
  line-height: 1.6;
}

.home-btn {
  height: 48px;
  padding: 0 48px;
  font-size: 16px;
  font-weight: 500;
  background: #00bcd4;
  border: none;
  color: #ffffff;
}

.home-btn:hover {
  background: #00acc1;
}

/* 账号展示 */
.accounts-container {
  width: 100%;
}

.accounts-card {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #333333;
  margin: 0;
}

.one-time-alert {
  margin-bottom: 16px;
}

.destroyed-alert {
  margin-bottom: 24px;
}

/* 内容显示 */
.content-display {
  background: #fafafa;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 20px;
  max-height: 500px;
  overflow-y: auto;
}

.content-display pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #333333;
}

.content-display::-webkit-scrollbar {
  width: 8px;
}

.content-display::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}

.content-display::-webkit-scrollbar-thumb {
  background: #d9d9d9;
  border-radius: 4px;
}

.content-display::-webkit-scrollbar-thumb:hover {
  background: #bfbfbf;
}

/* 操作按钮 */
.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 120px;
  height: 48px;
  font-size: 15px;
  font-weight: 500;
}

.action-btn:first-child {
  background: #00bcd4;
  border: none;
  color: #ffffff;
}

.action-btn:first-child:hover {
  background: #00acc1;
}

.destroy-btn {
  background: #ff4d4f !important;
  border-color: #ff4d4f !important;
  color: #ffffff !important;
}

.destroy-btn:hover {
  background: #ff7875 !important;
  border-color: #ff7875 !important;
}

/* 安全提示 */
.security-alert {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
}

.security-alert :deep(.ant-alert-icon) {
  color: #00bcd4;
}

.security-alert :deep(.ant-alert-message) {
  color: #333333;
  font-size: 16px;
  font-weight: 600;
}

.alert-content {
  color: #666666;
  font-size: 14px;
  line-height: 1.6;
}

.alert-content p {
  margin: 4px 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .link-page {
    padding: 24px 16px;
  }

  .expired-card {
    padding: 40px 20px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}
</style>