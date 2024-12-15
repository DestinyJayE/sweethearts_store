// api/user.js
import {USER_BASE_URL} from '@/constants'

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
}

export default UserAPI