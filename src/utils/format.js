// 格式化账号为文本
export const formatAccountsText = (accounts) => {
  if (!accounts || accounts.length === 0) {
    return '';
  }

  return accounts.map(acc => {
    return acc.password ? `${acc.username}|${acc.password}` : acc.username;
  }).join('\n');
};

// 复制到剪贴板
export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('复制失败:', err);
    return false;
  }
};

// 下载为txt文件
export const downloadAsTxt = (accounts, filename = 'accounts.txt') => {
  const text = formatAccountsText(accounts);
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};