import os

##########################################
# 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
# 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
AK = os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
SK = os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
# AK = ''  # 代码内手动输入并不安全，请确保代码不会被泄露
# SK = ''  # 代码内手动输入并不安全，请确保代码不会被泄露

