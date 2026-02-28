<template>
  <div class="create-page">
    <div class="container">
      <a-card class="create-card">
        <div class="card-header">
          <h1 class="title">创建账号分发链接</h1>
          <p class="subtitle">生成可设置有效期的账号分享链接</p>
        </div>

        <a-form layout="vertical" @submit="handleSubmit">
          <a-form-item label="账号列表" required>
            <div class="form-tip">无需注重格式</div>
            <a-textarea
              v-model:value="form.accounts"
              placeholder="此处的文本将在生成的链接内将完整展示"
              :rows="8"
              class="accounts-input"
            />
          </a-form-item>

          <a-form-item label="链接有效期" required>
            <a-select
              v-model:value="form.expireHours"
              size="large"
              class="expire-select"
            >
              <a-select-option :value="0.5">30 分钟</a-select-option>
              <a-select-option :value="1">1 小时</a-select-option>
              <a-select-option :value="2">2 小时</a-select-option>
              <a-select-option :value="6">6 小时</a-select-option>
              <a-select-option :value="12">12 小时</a-select-option>
              <a-select-option :value="24">24 小时</a-select-option>
            </a-select>
          </a-form-item>

          <a-form-item>
            <a-checkbox v-model:checked="form.oneTime" class="one-time-checkbox">
              一次性链接
            </a-checkbox>
            <div v-if="form.oneTime" class="one-time-warning">
              <a-alert
                type="warning"
                show-icon
                message="警告"
                description="任何人首次查看此链接后，链接将立即失效且无法再次访问。请确保接收者能及时保存账号信息。"
              />
            </div>
          </a-form-item>

          <a-form-item>
            <a-checkbox
              v-model:checked="form.allowDestroy"
              class="allow-destroy-checkbox"
              :disabled="form.oneTime"
            >
              允许查看者销毁链接
            </a-checkbox>
            <div v-if="form.allowDestroy" class="allow-destroy-info">
              <a-alert
                type="info"
                show-icon
                message="说明"
                description="查看者可以点击'销毁链接'按钮主动使链接失效，表示'我已保存好账号信息，请销毁'。"
              />
            </div>
            <div v-if="form.oneTime" class="allow-destroy-disabled-hint">
              <a-alert
                type="info"
                show-icon
                message="提示"
                description="一次性链接在首次查看后会自动失效，无需手动销毁。"
              />
            </div>
          </a-form-item>

          <a-form-item label="查看密码">
            <a-input-group compact>
              <a-input
                v-model:value="form.viewPassword"
                placeholder="不设置则无需密码（存在安全风险）"
                :type="showPassword ? 'text' : 'password'"
                class="password-input"
              />
              <a-button @click="showPassword = !showPassword" class="toggle-password-btn">
                {{ showPassword ? '隐藏' : '显示' }}
              </a-button>
              <a-button @click="generateRandomPassword" class="generate-password-btn">
                随机生成
              </a-button>
            </a-input-group>
            <div v-if="!form.viewPassword" class="password-warning">
              <a-alert
                type="warning"
                show-icon
                message="安全提醒"
                description="未设置查看密码，任何知道链接的人都可以访问账号信息，存在安全风险。"
              />
            </div>
          </a-form-item>

          <a-form-item>
            <a-button
              type="primary"
              size="large"
              block
              :loading="loading"
              @click="handleSubmit"
              class="submit-btn"
            >
              生成分发链接
            </a-button>
          </a-form-item>
        </a-form>

        <!-- 成功结果 -->
        <div v-if="result" class="result-section">
          <a-divider>链接已生成</a-divider>
          <div class="result-content">
            <div class="link-input-group">
              <a-input
                :value="fullLink"
                readonly
                size="large"
                class="link-input"
              />
              <a-button
                type="primary"
                size="large"
                @click="handleCopy"
                class="copy-btn"
              >
                复制链接
              </a-button>
            </div>
            <div v-if="form.viewPassword" class="link-input-group">
              <a-input
                :value="fullLinkWithPassword"
                readonly
                size="large"
                class="link-input"
              />
              <a-button
                type="primary"
                size="large"
                @click="handleCopyWithPassword"
                class="copy-btn"
              >
                复制链接（含密码）
              </a-button>
            </div>
            <div class="result-info">
              <a-tag color="green">链接有效期：{{ formatExpireTime(form.expireHours) }}</a-tag>
              <a-tag v-if="form.oneTime" color="orange">一次性链接</a-tag>
              <a-tag v-if="form.allowDestroy" color="purple">可销毁</a-tag>
              <a-tag v-if="form.viewPassword" color="cyan">有密码保护</a-tag>
              <a-tag v-else color="red">无密码保护</a-tag>
            </div>
            <div class="result-actions">
              <a-button @click="handleOpenLink" type="link" size="large">
                打开链接
              </a-button>
              <a-button @click="handleReset" type="link" size="large">
                创建新链接
              </a-button>
            </div>
          </div>
        </div>
      </a-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { message } from 'ant-design-vue';
import { useRouter } from 'vue-router';
import { createLink } from '../api';
import { copyToClipboard } from '../utils/format';

const router = useRouter();

const form = ref({
  accounts: '',
  expireHours: 0.5,
  oneTime: false,
  allowDestroy: false,
  viewPassword: ''
});

const showPassword = ref(false);

// 监听一次性链接选项变化
watch(() => form.value.oneTime, (newValue) => {
  if (newValue) {
    // 勾选一次性链接时，自动取消勾选主动销毁
    form.value.allowDestroy = false;
  }
});

const loading = ref(false);
const result = ref(null);

const fullLink = computed(() => {
  if (!result.value) return '';
  return `${window.location.origin}/link/${result.value.uuid}`;
});

const fullLinkWithPassword = computed(() => {
  if (!result.value || !form.value.viewPassword) return '';
  return `${window.location.origin}/link/${result.value.uuid}?pwd=${encodeURIComponent(form.value.viewPassword)}`;
});

const formatExpireTime = (hours) => {
  if (hours < 1) {
    return `${Math.round(hours * 60)} 分钟`;
  }
  return `${hours} 小时`;
};

const handleSubmit = async () => {
  // 验证
  if (!form.value.accounts.trim()) {
    message.error('请输入内容');
    return;
  }

  loading.value = true;

  try {
    const data = await createLink(form.value.accounts, form.value.expireHours, form.value.oneTime, form.value.allowDestroy, form.value.viewPassword);
    result.value = data;
    message.success('链接创建成功！');
  } catch (error) {
    message.error(error.error || '创建链接失败');
  } finally {
    loading.value = false;
  }
};

const handleCopy = async () => {
  const success = await copyToClipboard(fullLink.value);
  if (success) {
    message.success('链接已复制到剪贴板');
  } else {
    message.error('复制失败');
  }
};

const handleCopyWithPassword = async () => {
  const success = await copyToClipboard(fullLinkWithPassword.value);
  if (success) {
    message.success('链接（含密码）已复制到剪贴板');
  } else {
    message.error('复制失败');
  }
};

const generateRandomPassword = () => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
  let password = '';
  for (let i = 0; i < 12; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  form.value.viewPassword = password;
  message.success('已生成随机密码');
};

const handleOpenLink = () => {
  if (result.value) {
    router.push(`/link/${result.value.uuid}`);
  }
};

const handleReset = () => {
  form.value.accounts = '';
  form.value.expireHours = 0.5;
  form.value.oneTime = false;
  form.value.allowDestroy = false;
  form.value.viewPassword = '';
  showPassword.value = false;
  result.value = null;
};
</script>

<style scoped>
.create-page {
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

.create-card {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
}

.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: #666666;
  margin: 0;
}

.form-tip {
  font-size: 12px;
  color: #666666;
  margin-bottom: 8px;
}

.accounts-input {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
}

.accounts-input :deep(textarea) {
  background: #ffffff;
  border-color: #d9d9d9;
  color: #333333;
}

.accounts-input :deep(textarea:focus) {
  border-color: #00bcd4;
  box-shadow: 0 0 0 2px rgba(0, 188, 212, 0.1);
}

.expire-select {
  width: 100%;
}

.submit-btn {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  background: #00bcd4;
  border: none;
  color: #ffffff;
}

.submit-btn:hover {
  background: #00acc1;
}

.result-section {
  margin-top: 24px;
}

.result-content {
  padding: 20px 0;
}

.link-input-group {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.link-input {
  flex: 1;
  font-family: 'Consolas', 'Monaco', monospace;
}

.link-input :deep(input) {
  background: #ffffff;
  border-color: #d9d9d9;
  color: #333333;
}

.copy-btn {
  white-space: nowrap;
  background: #00bcd4;
  border: none;
  color: #ffffff;
}

.copy-btn:hover {
  background: #00acc1;
}

.result-info {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.result-actions {
  display: flex;
  gap: 24px;
  justify-content: center;
}

.result-actions :deep(.ant-btn-link) {
  color: #00bcd4;
}

.result-actions :deep(.ant-btn-link:hover) {
  color: #00acc1;
}

.one-time-checkbox {
  font-size: 14px;
  color: #333333;
}

.one-time-warning {
  margin-top: 12px;
}

.allow-destroy-checkbox {
  font-size: 14px;
  color: #333333;
}

.allow-destroy-info {
  margin-top: 12px;
}

.allow-destroy-disabled-hint {
  margin-top: 12px;
}

.password-input {
  flex: 1;
}

.toggle-password-btn,
.generate-password-btn {
  flex-shrink: 0;
}

.password-warning {
  margin-top: 12px;
}

/* 响应式 */
@media (max-width: 768px) {
  .create-page {
    padding: 24px 16px;
  }

  .link-input-group {
    flex-direction: column;
  }

  .copy-btn {
    width: 100%;
  }
}
</style>