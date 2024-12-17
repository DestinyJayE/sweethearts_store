// api/task.js
import { TASK_BASE_URL } from '@/constants'
import { request } from '@/utils/request'

class TaskAPI{
    static getSelfTasks(){
        return request.get(TASK_BASE_URL + '/self_task')
    }

    static getSweetheartTask(){
        return request.get(TASK_BASE_URL + '/sweetheart_task')
    }

    static addTask(data){
        return request.post(TASK_BASE_URL + '/add', data)
    }

    static deleteTask(id){
        return request.post(TASK_BASE_URL + '/delete/?id=' + id)
    }

    static finishTask(id){
        return request.post(TASK_BASE_URL + '/finish/?id=' + id)
    }

}

export default TaskAPI