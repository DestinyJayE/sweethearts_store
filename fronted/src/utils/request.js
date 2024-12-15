import axios from 'axios'
import {BASE_URL} from '@/components'

const service = axios.create({
    baseURL: BASE_URL,
    timeout: 50000,
    headers: {'Content-Type': 'application/json;charset=utf-8'}
})

export default service