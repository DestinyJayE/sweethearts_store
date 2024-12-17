// api/user.js
import {USER_BASE_URL} from '@/constants'
import { request } from '@/utils/request'

class UserAPI {
    /**
     * 登录
     */
    static login(data){
        return request({
            url: `${USER_BASE_URL}/login`,
            method: `post`,
            data
        })
    }

    static getPoint(){
        return request.get(`${USER_BASE_URL}/point`)
    }

    static getSweetheartPoint(){
        return request.get(`${USER_BASE_URL}/sweetheart_point`)
    }
}

export default UserAPI
