import os
import sys

from typing import List

from alibabacloud_swas_open20200601.client import Client as SWAS_OPEN20200601Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_swas_open20200601 import models as swas__open20200601_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from config import *


def list_plans(region_id='cn-hongkong', core=2, memory=2, support_platform='Linux', disk_type='ESSD'):
    """列出某区域中的套餐情况

    :param region_id: 地区id。 默认为香港
    :param core: vCPU核数。 默认为2
    :param mamory: 内存大小。 默认为2GB
    :param support_platform: 支持的系统。 默认为Linux
    :param disk_type: 磁盘类型。 默认为ESSD，也是web页面中默认出现的，也更便宜
    :return: 
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
    list_plans_request = swas__open20200601_models.ListPlansRequest(
        region_id=region_id
    )
    runtime = util_models.RuntimeOptions()
    plans = []
    try:
        result = client.list_plans_with_options(list_plans_request, runtime)
        for plan in result.body.plans:
            # print(plan)  # 筛选前可以先都打印出来看看
            if (support_platform in plan.support_platform) and (plan.disk_type == disk_type) and \
                (plan.core == core) and (plan.memory == memory):
                # print(plan)
                plans.append(plan)

        return plans
    except Exception as error:
        err_str = UtilClient.assert_as_string(error.message)    
        print(err_str)


if __name__ == '__main__':
    plans = list_plans()
    for plan in plans:
        print(plan)
        # 找到指定的 plan_id
        if plan.origin_price == '34':  # 我这里使用价格再次确认
            print(plan.plan_id)

