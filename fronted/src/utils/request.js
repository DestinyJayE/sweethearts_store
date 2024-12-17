// utils/request.js
import axios from 'axios';
import { BASE_URL } from '@/constants';

import { ElMessage } from 'element-plus';

const service = axios.create({
    baseURL: BASE_URL,
    timeout: 50000,
    headers: { 'Content-Type': 'application/json;charset=utf-8' },
});

const pendingMap = new Map()

// 添加拦截器（可选）
service.interceptors.response.use(
    response => {
        // 成功处理逻辑
        removePending(response.config);
        
        const { code, data, msg } = response.data;
        console.log(code)
        if (code === '200') {
            return data;
        }else if(code === '429'){
            ElMessage.error(msg);
            return
        } 
        ElMessage.error(msg || '请求失败');
    },
    error => {
        if (error.config) {
            removePending(error.config);
        }

        let errorMessage = '';
        if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
            // 处理超时错误
            errorMessage = '请求超时，请稍后重试。';
        }
        else if (error.response) {
            // 服务器响应了请求，但状态码不在 2xx 范围内
            const { status, data } = error.response;
            if (status === 401 || (data && data.code === 'TOKEN_EXPIRED')) {
                window.dispatchEvent(new Event('token-expired'));
                window.location.href = '/login';
                errorMessage = '登录已过期，请重新登录';
            } else {
                errorMessage = data?.msg || `请求失败，状态码 ${status}`;
            }
        } else {
            // 没有响应或者请求被阻止
            errorMessage = '网络错误或请求被中断。';
        }

        ElMessage.error(errorMessage);
        ElMessage.error({
            message: errorMessage,
            position: 'top'
          });
        console.error(error);
    }
);


service.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});
/**
 * 删除重复的请求
 * @param {*} config
 */
function removePending(config) {
    const pendingKey = getPendingKey(config)
    if (pendingMap.has(pendingKey)) {
        const cancelToken = pendingMap.get(pendingKey)
        cancelToken(pendingKey)
        pendingMap.delete(pendingKey)
    }
}

/**
 * 生成唯一的每个请求的唯一key
 * @param {*} config
 * @returns
 */
function getPendingKey(config) {
    let { url, method, params, data } = config
    if (typeof data === 'string') data = JSON.parse(data) // response里面返回的config.data是个字符串对象
    return [url, method, JSON.stringify(params), JSON.stringify(data)].join('&')
}

export const request = service;