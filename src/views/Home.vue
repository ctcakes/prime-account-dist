<template>
  <div class="home-page">
    <!-- Hero 区域 -->
    <section class="hero-section">
      <div class="hero-container">
        <h1 class="hero-title">Prime Account Dist</h1>
        <p class="hero-subtitle">官匹账号安全分发工具</p>
        <p class="hero-description">用于官匹死号后的账号分发</p>
        <div class="hero-buttons">
          <a-button type="primary" size="large" class="btn-primary" @click="goToCreate">创建分发链接</a-button>
          <a-button size="large" class="btn-secondary">查看 GitHub</a-button>
        </div>
      </div>
    </section>

    <!-- 问题背景说明区 -->
    <section class="problem-section">
      <div class="section-container">
        <h2 class="section-title">为什么需要这个工具</h2>
        <div class="problem-content">
          <div class="problem-item">
            <div class="problem-icon">
              <WarningOutlined />
            </div>
            <div class="problem-text">
              <h3>VAC 连坐赔偿</h3>
              <p>官匹组排中，若出现 VAC 连坐情况，责任方需要补偿其他受影响玩家</p>
            </div>
          </div>
          <div class="problem-item">
            <div class="problem-icon">
              <MailOutlined />
            </div>
            <div class="problem-text">
              <h3>手动分发很麻烦</h3>
              <p>通过聊天软件直接发送账号信息非常麻烦，且群聊无法发起临时会话</p>
            </div>
          </div>
          <div class="problem-item">
            <div class="problem-icon">
              <ClockCircleOutlined />
            </div>
            <div class="problem-text">
              <h3>有效期难以控制</h3>
              <p>传统方式无法设置账号使用有效期，可能导致账号被滥用</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 解决方案说明区 -->
    <section class="solution-section">
      <div class="section-container">
        <h2 class="section-title">解决方案</h2>
        <div class="solution-steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>上传补偿账号</h3>
            <p>将需要补偿的账号信息录入系统</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>生成专属链接</h3>
            <p>系统自动生成唯一的访问链接</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>设置有效期</h3>
            <p>自定义链接的有效使用时长</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step">
            <div class="step-number">4</div>
            <h3>安全分发</h3>
            <p>被补偿者输入密码获取账号信息</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 核心特点展示区 -->
    <section class="features-section">
      <div class="section-container">
        <h2 class="section-title">核心特点</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <UnlockOutlined />
            </div>
            <h3>开源透明</h3>
            <p>完全开源，代码可审计</p>
            <a href="#" class="feature-link">查看源码 →</a>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <DeleteOutlined />
            </div>
            <h3>不存储长期数据</h3>
            <p>数据短期存储，自动清理</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <SafetyOutlined />
            </div>
            <h3>不偷账号</h3>
            <p>代码完全开源，你可以自己搭自己用。我们也看不上你的账号</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <RocketOutlined />
            </div>
            <h3>简单部署</h3>
            <p>快速部署，易于维护</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <FieldTimeOutlined />
            </div>
            <h3>可控有效期</h3>
            <p>灵活设置链接使用时长</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <LockOutlined />
            </div>
            <h3>安全可靠</h3>
            <p>多重保障，数据安全</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 安全声明区 -->
    <section class="security-section">
      <div class="section-container">
        <h2 class="section-title">安全声明</h2>
        <div class="security-content">
          <div class="security-item">
            <a-checkbox checked disabled></a-checkbox>
            <p>本项目完全开源，所有代码公开可查</p>
          </div>
          <div class="security-item">
            <a-checkbox checked disabled></a-checkbox>
            <p>代码可自行审计，确保无后门</p>
          </div>
          <div class="security-item">
            <a-checkbox checked disabled></a-checkbox>
            <p>不会窃取或保存任何账号数据</p>
          </div>
          <div class="security-item">
            <a-checkbox checked disabled></a-checkbox>
            <p>不进行任何远程上传或隐藏通信</p>
          </div>
        </div>
        <div class="security-cta">
          <p>请自行审查源码，确保安全后再使用</p>
          <a-button type="primary" size="large" class="btn-github">
            GitHub 仓库
          </a-button>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-links">
          <a href="#" class="footer-link">GitHub 仓库</a>
          <span class="footer-divider">|</span>
          <span class="footer-text">开源项目</span>
        </div>
        <div class="footer-copyright">
          © 2026 Prime Account Dist. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import {
  WarningOutlined,
  MailOutlined,
  ClockCircleOutlined,
  UnlockOutlined,
  DeleteOutlined,
  SafetyOutlined,
  RocketOutlined,
  FieldTimeOutlined,
  LockOutlined
} from '@ant-design/icons-vue';

const router = useRouter();

const goToCreate = () => {
  router.push('/create');
};
</script>

<style scoped>
/* 全局样式 */
.home-page {
  min-height: 100vh;
  background: #f5f5f5;
  color: #333333;
}

/* 通用容器 */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-title {
  font-size: 32px;
  font-weight: 600;
  text-align: center;
  color: #333333;
  margin-bottom: 48px;
}

/* Hero 区域 */
.hero-section {
  padding: 100px 24px 80px;
  background: #ffffff;
  border-bottom: 1px solid #e8e8e8;
}

.hero-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  color: #333333;
  margin-bottom: 16px;
  letter-spacing: -0.5px;
}

.hero-subtitle {
  font-size: 24px;
  color: #00bcd4;
  margin-bottom: 12px;
  font-weight: 500;
}

.hero-description {
  font-size: 18px;
  color: #666666;
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn-primary {
  height: 48px;
  padding: 0 32px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 4px;
  background: #00bcd4;
  border: none;
  color: #ffffff;
}

.btn-primary:hover {
  background: #00acc1;
}

.btn-secondary {
  height: 48px;
  padding: 0 32px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  color: #333333;
}

.btn-secondary:hover {
  border-color: #00bcd4;
  color: #00bcd4;
}

/* 问题背景说明区 */
.problem-section {
  padding: 80px 24px;
  background: #f5f5f5;
}

.problem-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.problem-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding: 24px;
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
}

.problem-icon {
  font-size: 32px;
  flex-shrink: 0;
  color: #00bcd4;
}

.problem-text h3 {
  font-size: 20px;
  color: #333333;
  margin-bottom: 8px;
  font-weight: 600;
}

.problem-text p {
  font-size: 15px;
  color: #666666;
  line-height: 1.6;
}

/* 解决方案说明区 */
.solution-section {
  padding: 80px 24px;
  background: #ffffff;
  border-top: 1px solid #e8e8e8;
  border-bottom: 1px solid #e8e8e8;
}

.solution-steps {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.step {
  flex: 1;
  min-width: 200px;
  text-align: center;
  padding: 32px 24px;
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
}

.step-number {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  background: #00bcd4;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
}

.step h3 {
  font-size: 18px;
  color: #333333;
  margin-bottom: 8px;
  font-weight: 600;
}

.step p {
  font-size: 14px;
  color: #666666;
  line-height: 1.5;
}

.step-arrow {
  font-size: 24px;
  color: #00bcd4;
  padding: 0 10px;
}

/* 核心特点展示区 */
.features-section {
  padding: 80px 24px;
  background: #f5f5f5;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.feature-card {
  padding: 32px;
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  border-color: #00bcd4;
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 16px;
  color: #00bcd4;
}

.feature-card h3 {
  font-size: 18px;
  color: #333333;
  margin-bottom: 12px;
  font-weight: 600;
}

.feature-card p {
  font-size: 14px;
  color: #666666;
  line-height: 1.5;
  margin-bottom: 16px;
}

.feature-link {
  color: #00bcd4;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.feature-link:hover {
  color: #00acc1;
  text-decoration: underline;
}

/* 安全声明区 */
.security-section {
  padding: 80px 24px;
  background: #ffffff;
  border-top: 1px solid #e8e8e8;
}

.security-content {
  max-width: 800px;
  margin: 0 auto 48px;
}

.security-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  margin-bottom: 12px;
}

.security-item p {
  font-size: 15px;
  color: #333333;
  margin: 0;
  line-height: 1.5;
}

.security-cta {
  text-align: center;
}

.security-cta p {
  font-size: 14px;
  color: #666666;
  margin-bottom: 24px;
}

.btn-github {
  height: 48px;
  padding: 0 48px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 4px;
  background: #00bcd4;
  border: none;
  color: #ffffff;
}

.btn-github:hover {
  background: #00acc1;
}

/* 页脚 */
.footer {
  padding: 40px 24px;
  background: #fafafa;
  border-top: 1px solid #e8e8e8;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.footer-link {
  color: #00bcd4;
  text-decoration: none;
  font-size: 14px;
}

.footer-link:hover {
  color: #00acc1;
  text-decoration: underline;
}

.footer-divider {
  color: #bfbfbf;
}

.footer-text {
  color: #666666;
  font-size: 14px;
}

.footer-copyright {
  color: #999999;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 40px;
  }

  .hero-subtitle {
    font-size: 20px;
  }

  .hero-description {
    font-size: 16px;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .step-arrow {
    transform: rotate(90deg);
  }

  .footer-container {
    flex-direction: column;
    text-align: center;
  }
}
</style>