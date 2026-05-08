/**
 * CRM 系统前端交互脚本
 * 功能：表单验证、加载动画、AJAX 提交、图表初始化
 */

document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有功能
    initFormValidation();
    initLoadingOverlay();
    initAlerts();
    initCharts();
    initMobileMenu();
});

/**
 * 表单实时验证
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(function(form) {
        const inputs = form.querySelectorAll('.form-control');
        
        inputs.forEach(function(input) {
            // 失去焦点时验证
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            // 输入时移除错误状态
            input.addEventListener('input', function() {
                if (input.classList.contains('is-invalid')) {
                    input.classList.remove('is-invalid');
                    const feedback = input.parentNode.querySelector('.invalid-feedback');
                    if (feedback) feedback.style.display = 'none';
                }
            });
        });
        
        // 表单提交验证
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            event.stopPropagation();
            
            let isValid = true;
            inputs.forEach(function(input) {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (isValid) {
                // 显示加载动画
                showLoading('正在提交...');
                
                // 如果是 AJAX 表单，执行 AJAX 提交
                if (form.classList.contains('ajax-form')) {
                    submitFormAjax(form);
                } else {
                    form.submit();
                }
            } else {
                // 滚动到第一个错误字段
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
            }
        }, false);
    });
}

/**
 * 验证单个字段
 */
function validateField(field) {
    let isValid = true;
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');
    const minLength = field.getAttribute('minlength');
    const maxLength = field.getAttribute('maxlength');
    const pattern = field.getAttribute('pattern');
    
    // 清空之前的状态
    field.classList.remove('is-valid', 'is-invalid');
    
    // 必填验证
    if (required && !value) {
        isValid = false;
        showFieldError(field, '此字段为必填项');
        return isValid;
    }
    
    // 如果为空但不是必填，跳过其他验证
    if (!value) {
        return true;
    }
    
    // 最小长度验证
    if (minLength && value.length < parseInt(minLength)) {
        isValid = false;
        showFieldError(field, `最少需要${minLength}个字符`);
        return isValid;
    }
    
    // 最大长度验证
    if (maxLength && value.length > parseInt(maxLength)) {
        isValid = false;
        showFieldError(field, `最多允许${maxLength}个字符`);
        return isValid;
    }
    
    // 正则表达式验证
    if (pattern) {
        const regex = new RegExp(pattern);
        if (!regex.test(value)) {
            isValid = false;
            const messages = {
                '^[1][3-9]\\d{9}$': '请输入正确的手机号',
                '^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$': '请输入正确的邮箱地址',
                '^\\d+$': '请输入数字',
                '^\\d+\\.\\d{2}$': '请输入正确的金额格式（如：100.00）'
            };
            showFieldError(field, messages[pattern] || '格式不正确');
            return isValid;
        }
    }
    
    // 邮箱验证
    if (type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            showFieldError(field, '请输入正确的邮箱地址');
            return isValid;
        }
    }
    
    // 电话验证
    if (type === 'tel' || field.name === 'phone' || field.name === 'qq') {
        if (field.name === 'phone') {
            const phoneRegex = /^1[3-9]\d{9}$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                showFieldError(field, '请输入正确的手机号');
                return isValid;
            }
        }
        if (field.name === 'qq') {
            const qqRegex = /^[1-9]\d{4,10}$/;
            if (!qqRegex.test(value)) {
                isValid = false;
                showFieldError(field, '请输入正确的 QQ 号');
                return isValid;
            }
        }
    }
    
    // 验证通过
    if (isValid) {
        field.classList.add('is-valid');
        const feedback = field.parentNode.querySelector('.valid-feedback');
        if (feedback) feedback.style.display = 'block';
    }
    
    return isValid;
}

/**
 * 显示字段错误信息
 */
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    let feedback = field.parentNode.querySelector('.invalid-feedback');
    
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentNode.appendChild(feedback);
    }
    
    feedback.textContent = message;
    feedback.style.display = 'block';
}

/**
 * 加载动画覆盖层
 */
function initLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (!overlay) {
        const html = `
            <div id="loadingOverlay" class="loading-overlay">
                <div class="loading-content">
                    <div class="spinner"></div>
                    <div class="loading-text">加载中...</div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', html);
    }
}

function showLoading(text = '加载中...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = overlay.querySelector('.loading-text');
    loadingText.textContent = text;
    overlay.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('active');
}

/**
 * AJAX 表单提交
 */
function submitFormAjax(form) {
    const formData = new FormData(form);
    const actionUrl = form.action || window.location.href;
    const method = (form.method || 'POST').toUpperCase();
    
    fetch(actionUrl, {
        method: method,
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            showAlert('success', data.message || '操作成功');
            if (data.redirect_url) {
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1500);
            }
        } else {
            showAlert('danger', data.message || '操作失败');
            if (data.errors) {
                Object.keys(data.errors).forEach(fieldName => {
                    const field = form.querySelector(`[name="${fieldName}"]`);
                    if (field) {
                        showFieldError(field, data.errors[fieldName][0]);
                    }
                });
            }
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        showAlert('danger', '网络错误，请稍后重试');
    });
}

/**
 * 获取 CSRF Token
 */
function getCsrfToken() {
    let token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) {
        return token.value;
    }
    token = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return token ? token.split('=')[1] : '';
}

/**
 * 警报消息管理
 */
function initAlerts() {
    // 自动关闭警报
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            closeAlert(alert);
        }, 5000);
    });
}

function showAlert(type, message) {
    // 移除现有警报
    const existingAlert = document.querySelector('.alert-container .alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="close" onclick="closeAlert(this.parentElement)">
                <span>&times;</span>
            </button>
        </div>
    `;
    
    let container = document.querySelector('.alert-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'alert-container';
        const mainContent = document.querySelector('.container') || document.body;
        mainContent.insertBefore(container, mainContent.firstChild);
    }
    
    container.insertAdjacentHTML('afterbegin', alertHtml);
    
    // 滚动到顶部显示警报
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function closeAlert(alert) {
    alert.classList.remove('show');
    setTimeout(() => {
        alert.remove();
    }, 300);
}

/**
 * 图表初始化 (使用 Chart.js)
 */
function initCharts() {
    // 检查是否有图表容器
    const chartContainers = document.querySelectorAll('.chart-container');
    if (chartContainers.length === 0) return;
    
    // 动态加载 Chart.js
    if (typeof Chart === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js';
        script.onload = () => createCharts();
        document.head.appendChild(script);
    } else {
        createCharts();
    }
}

function createCharts() {
    // 客户来源分布图
    const sourceChartEl = document.getElementById('sourceChart');
    if (sourceChartEl) {
        const ctx = sourceChartEl.getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['线上咨询', '电话咨询', '客户介绍', '地推活动', '其他'],
                datasets: [{
                    data: [35, 25, 20, 15, 5],
                    backgroundColor: [
                        '#4e73df',
                        '#1cc88a',
                        '#36b9cc',
                        '#f6c23e',
                        '#858796'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // 月度业绩趋势图
    const trendChartEl = document.getElementById('trendChart');
    if (trendChartEl) {
        const ctx = trendChartEl.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1 月', '2 月', '3 月', '4 月', '5 月', '6 月'],
                datasets: [{
                    label: '成交额',
                    data: [12000, 19000, 15000, 25000, 22000, 30000],
                    borderColor: '#4e73df',
                    backgroundColor: 'rgba(78, 115, 223, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

/**
 * 移动端菜单切换
 */
function initMobileMenu() {
    const menuToggle = document.querySelector('.navbar-toggler');
    const navbarNav = document.querySelector('.navbar-nav');
    
    if (menuToggle && navbarNav) {
        menuToggle.addEventListener('click', function() {
            navbarNav.classList.toggle('show');
        });
    }
}

/**
 * 表格行点击效果
 */
function initTableInteraction() {
    const tables = document.querySelectorAll('.table-hover tbody tr');
    tables.forEach(row => {
        row.addEventListener('click', function() {
            // 可以在这里添加行点击后的操作
            console.log('Row clicked:', this);
        });
    });
}

/**
 * 确认删除对话框
 */
function confirmDelete(message = '确定要删除吗？此操作不可恢复！') {
    return confirm(message);
}

/**
 * 数字格式化
 */
function formatNumber(num, decimals = 2) {
    return Number(num).toFixed(decimals).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

/**
 * 日期格式化
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}`;
}

// 导出函数供外部调用
window.CRMUtils = {
    showLoading,
    hideLoading,
    showAlert,
    validateField,
    confirmDelete,
    formatNumber,
    formatDate
};
