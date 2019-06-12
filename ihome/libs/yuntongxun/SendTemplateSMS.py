#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-
import json

from ihome.libs.yuntongxun.CCPRestSDK import REST
#import ConfigParser

#主帐号
accountSid= '8aaf07086b211c22016b2b90bd160792'

#主帐号Token
accountToken= '710e210a203b4f2289c8f828adb1251f'

#应用Id
appId='8aaf07086b211c22016b2b90bd7a0799'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id
class CCP(object):
    #使用单例模式，判断是否有已经创建好的对象，保证初始化只执行一次
    ##__init__()负责将类的实例化，而在__init__()启动之前，__new__()决定是否 要使用该__init__()方法，因为__new__()可以调用其他类的构造方法或者直接返回别的对象来作为本类 的实例
    ##用来保存对象的类属性
    isinstance=None
    def __new__(cls):
        if cls.isinstance is None:
            obj=super(CCP,cls).__new__(cls)
            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.isinstance=obj
        return obj

    def sendTemplateSMS(self,to,datas,tempId):
        results = self.rest.sendTemplateSMS(to,datas,tempId)
        print(results)
        status_code=results.get("statusCode")
        if status_code=="000000":
            #发送成功
            return 0
        else:
            return -1
    

if __name__ == '__main__':
    cpp=CCP()
    cpp.sendTemplateSMS("13688815040",["768","3"],1)
#sendTemplateSMS(手机号码,内容数据,模板Id)