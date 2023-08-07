import os
import sys
import time

from typing import List

from alibabacloud_swas_open20200601.client import Client as SWAS_OPEN20200601Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_swas_open20200601 import models as swas__open20200601_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from config import *
from list_images import list_images
from list_plans import list_plans


def create_swas(image_id, plan_id, 
                period=1, amount=1, 
                auto_renew=True, auto_renew_period=1, 
                region_id='cn-hongkong',
                client_token='idempotence'):
    """创建轻量应用服务器

    :param image_id: 镜像ID。 通过 list_images.py 发现获取
    :param plan_id: 套餐ID。 通过 list_plans.py 发现获取
    :param period: 购买资源的时长。 单位：月。 取值范围：{"1", "3", "6", "12", "24", "36"}
    :param amount: 创建轻量应用服务器的数量。 取值范围：1~20
    :param auto_renew: 是否开启到期自动续费。 默认为True，到期自动续费
    :param auto_renew_period: 自动续费的时长，仅当AutoRenew=true时该参数必填。单位：月。取值范围：{"1", "3", "6", "12", "24", "36"}
    :param region_id: 地域ID。默认为'cn-hongkong'。您可以调用ListRegions查询可用地域。
    :param client_token: 保证请求幂等性。其他参数相同且该参数一致时，调用多次也仅创建一个实例。

    """

    ###############################
    # == 创建 API client
    config = open_api_models.Config(
        access_key_id=AK,
        access_key_secret=SK,
    )
    # Endpoint 请参考 https://api.aliyun.com/product/SWAS-OPEN
    config.endpoint = f'swas.cn-hongkong.aliyuncs.com'
    client = SWAS_OPEN20200601Client(config)

    ###############################
    # == 调用 API 
    create_instances_request = swas__open20200601_models.CreateInstancesRequest(
        region_id=region_id,
        image_id=image_id,
        plan_id=plan_id,
        amount=amount,
        period=period,
        auto_renew=auto_renew,
        auto_renew_period=auto_renew_period,
        client_token=client_token
    )
    runtime = util_models.RuntimeOptions()
    try:
        result = client.create_instances_with_options(create_instances_request, runtime)
        print(result)
        return result.status_code
    except Exception as error:
        err_str = UtilClient.assert_as_string(error.message)    
        print(err_str)


if __name__ == '__main__':

    # 找到指定的 image_id
    image_id = ''
    images = list_images(image_name='ubuntu')
    image_id = images['Ubuntu-20.04']

    # 找到指定的 plan_id
    plan_id = ''
    plans = list_plans()
    for plan in plans:
        if plan.origin_price == '34':  # 我这里使用价格再次确认
            plan_id = plan.plan_id

    print(image_id)
    print(plan_id)

    while True:
        status_code = create_swas(image_id, plan_id)
        if status_code == 200:
            break
        time.sleep(6)
