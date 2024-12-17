import { request } from '@/utils/request'
import {Goods_BASE_URL} from "@/constants";

class GoodsAPI{
    static getSelfGoods(){
        return request.get(Goods_BASE_URL+"/self_goods")
    }

    static getSweetheartGoods(){
        return request.get(Goods_BASE_URL+"/sweetheart_goods")
    }

    static buyGoods(goodsId){
        return request.post(Goods_BASE_URL+"/buy?id="+goodsId)
    }

    static deleteGoods(goodsId){
        return request.post(Goods_BASE_URL+"/delete?id="+goodsId)
    }

    static getBoughtGoods(){
        return request.get(Goods_BASE_URL+"/get_bought_goods")
    }
    static useGoods(id){
        return request.post(Goods_BASE_URL+"/use_goods?id="+id)
    }
}

export default GoodsAPI