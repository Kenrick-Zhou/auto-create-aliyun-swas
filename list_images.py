import os
import sys

from typing import List

from alibabacloud_swas_open20200601.client import Client as SWAS_OPEN20200601Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_swas_open20200601 import models as swas__open20200601_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from config import *


def list_images(region_id='cn-hongkong', image_name='', platform='Linux', image_type='system'):
    """列出某区域中的镜像情况

    :param region_id: 地区id。 默认为香港
    :param image_name: 查找镜像名称，包含，大小写敏感。 默认为空字符串，代表没有任何限制
    :param platfor: 系统平台。 默认Linux
    :param image_type: 镜像类型。 默认为system
    :return: key为镜像名称（区分大小写）， value为image_id的字典
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
    list_images_request = swas__open20200601_models.ListImagesRequest(
        region_id=region_id,
        image_type=image_type
    )
    runtime = util_models.RuntimeOptions()
    images = {}
    try:
        result = client.list_images_with_options(list_images_request, runtime)
        for image in result.body.images:
            # print(image)  # 筛选前可以先都打印出来看看
            if (image.platform == platform) and (image_name.lower() in image.image_name.lower()):
                # print(image)
                images[image.image_name] = image.image_id
                
        return images
    except Exception as error:
        err_str = UtilClient.assert_as_string(error.message)    
        print(err_str)


if __name__ == '__main__':
    images = list_images(image_name='ubuntu')
    for image_name in images.keys():
        print(f'{image_name}: {images[image_name]}')

    # 找到指定的 image_id
    print(images['Ubuntu-20.04'])
