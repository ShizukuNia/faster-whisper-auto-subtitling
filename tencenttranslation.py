import json
from typing import List
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

class Translation():
    def __init__(self) -> None:
        self.SecretId = "AKIDzoMdeOq1ue7JEtHODm45pIUP2QYPzHJ2"
        self.SecretKey = "TfbFciW3JHyOXPzJM8dqoVv84j7E4duu"
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        # AKIDzoMdeOq1ue7JEtHODm45pIUP2QYPzHJ2
        # TfbFciW3JHyOXPzJM8dqoVv84j7E4duu
        self.cred = credential.Credential(self.SecretId, self.SecretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "tmt.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        self.client = tmt_client.TmtClient(self.cred, "ap-shanghai", self.clientProfile)
        # 实例化一个请求对象,每个接口都会对应一个request对象
        self.req = models.TextTranslateBatchRequest()
        self.params = {
            "Source": "ja",
            "Target": "zh",
            "ProjectId": 0,
            "SourceTextList": ["ご視聴ありがとうございました"]
        }
            
    
    def translate(self, sourceTextList: List[str], source: str = "ja", target: str = "zh") -> str:
        self.params["SourceTextList"] = []
        self.params["Source"] = source
        self.params["Target"] = target
        self.params["SourceTextList"] = sourceTextList

        self.req.from_json_string(json.dumps(self.params))
        # 返回的resp是一个TextTranslateBatchResponse的实例，与请求对象对应
        resp = self.client.TextTranslateBatch(self.req)
        # 输出json格式的字符串回包
        #print(resp.to_json_string())
        resp_dict = json.loads(resp.to_json_string())
        resp_list = resp_dict["TargetTextList"]
        resp_text = ''.join(resp_list)
        print(f"翻译：{resp_text}")
        time.sleep(0.25)
        return resp_text
    
translation = Translation()
