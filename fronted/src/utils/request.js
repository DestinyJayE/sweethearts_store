// utils/request.js
import axios from 'axios';
import { BASE_URL } from '@/constants';

const service = axios.create({
    baseURL: BASE_URL,
    timeout: 50000,
    headers: { 'Content-Type': 'application/json;charset=utf-8' },
});

const pendingMap = new Map()

// 添加拦截器（可选）
service.interceptors.response.use(
    (response) => {
        removePending(response.config);
        const { code, data, msg } = response.data;
        if (code === '200') {
            return data;
        }
        return Promise.reject(new Error(msg || 'Error'));
    },
    (error) => {
        if (error.config) {
            removePending(error.config);
        }
        if (error.response) {
            const { status, data } = error.response;
            if (status === 401 || (data && data.code === 'TOKEN_EXPIRED')) {
                window.dispatchEvent(new Event('token-expired'));
                window.location.href = '/login';
                return Promise.reject(new Error('Token expired, please log in again.'));
            }
            return Promise.reject(new Error(data?.msg || `Request failed with status ${status}`));
        }
        return Promise.reject(new Error('Network error or request was aborted.'));
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