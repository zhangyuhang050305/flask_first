import json

from ronglian_sms_sdk import SmsSDK

accId = '2c94811c9dfd83b1019e4622f4522f72'
accToken = 'caaeb9a08c6f44a787fcc32d88b49f2b'
appId = '2c94811c9dfd83b1019e4622f4d02f79'

class CCP():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
            cls._instance.sdk = SmsSDK(accId, accToken, appId)
        return cls._instance

    def send_message(self,tid, mobile, datas, ):
        resp = json.loads(self.sdk.sendMessage(tid, mobile, datas))
        if resp.get('statusCode') == "000000":
            return 0
        else:
            return -1

if __name__ == '__main__':
    ccp = CCP()
    ccp.send_message('1', '18828698516', ('1234','4'))