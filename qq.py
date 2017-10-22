from selenium import webdriver
from multiprocessing import Process
from multiprocessing import Pool
import requests
import time
import sys
import os


class QianDao(object):

    #url_list[0]是大悦谷,url_list[1]是银号理财
    url_list = [
        "http://comm.ams.game.qq.com/ams/ame/ame.php?ameVersion=0.3&sServiceType=tgclub&iActivityId=116090&sServiceDepartment=xinyue&sSDID=06e8ae9a0469383ded2f9409e5e6db48&isXhrPost=true",\
        "http://comm.ams.game.qq.com/ams/ame/ame.php?ameVersion=0.3&sServiceType=tgclub&iActivityId=119640&sServiceDepartment=xinyue&sSDID=c907e097c54ea77d074705e141f4bad6&isXhrPost=true"   
    ]
    type_dict = {
        #任务名,iFlowId,param,iActivityId
        "fxkj" : ["380706","620711","116090"],
        "fxhy" : ["380706","620710","116090"],
        "mrqd" : ["378208","620717","116090"],
        "yhlc" : ["389635","1","119640"],
        "hqjf" : ["379876","116090"]
        }

    formData = {
        #"param" : "620717",
        "source" : "1",
        "sServiceType" : "tgclub",
        "iActivityId" : "116090",
        "iFlowId" : "378208",
        "g_tk" : "",
        "e_code" : "0",
        "g_code" : "0",
        "xhr" : "1",
        "sServiceDepartment" : "xinyue",
        "xhrPostKey" : "",
    }
    loginUrl = "http://xinyue.qq.com/act/pc/20170702week/index.html"
    chromePath = r"/Volumes/data/chromedriver"
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
            }


    session = requests.session()

    def __init__(self,login_uid,login_pwd):
        # 初始
        self.login_uid = login_uid
        self.login_pwd =login_pwd
        self.getCookie()
        self.huoquJiFen()
        self.oldJiFen = self.huoquJiFen()

        print(self.login_uid + ": #当前积分 " + str(self.oldJiFen) + "#")

    def __del__(self):
        currentJifen = self.huoquJiFen()
        print(self.login_uid + ": #当前积分 " + str(currentJifen) + "," + "获得积分 "  + str(currentJifen - self.oldJiFen) + "#")


    def fenxiangHaoYou(self):
        """
            分享到好友
        """
        print("-"*25 + "%s: 开始分享好友"%self.login_uid + "-"*25)
        #得到xhr
        playload = self.formData
        xhr = "xhr_" + str(int(time.time()*1000))
        #构建提交表单数据

        playload["xhrPostKey"] = xhr
        playload["iFlowId"] = self.type_dict["fxkj"][0]
        playload["param"] = self.type_dict["fxkj"][1]
        playload["iActivityId"] = self.type_dict["fxkj"][2]

        response = self.session.post(self.url_list[0],data=playload,headers=self.headers)
        self.print_msg(response)

        print("-"*25 + "%s: 分享好友结束"%self.login_uid + "-"*25)
        print("\n")

    def fenxiangKongJian(self):
        """
            分享到空间

        """

        print("-"*25 + "%s: 分享空间开始"%self.login_uid + "-"*25)
        playload = self.formData
        #得到xhr
        xhr = "xhr_" + str(int(time.time()*1000))
        playload["xhrPostKey"] = xhr
        #构建提交表单数据
        playload["iFlowId"] = self.type_dict["fxhy"][0]
        playload["param"] = self.type_dict["fxhy"][1]
        playload["iActivityId"] = self.type_dict["fxhy"][2]

        response = self.session.post(self.url_list[0],data=playload,headers=self.headers)
        self.print_msg(response)
        print("-"*25 + "%s: 分享空间结束"%self.login_uid + "-"*25)
        print("\n")


    def meiriQianDao(self):
        """
            每日签到
        """
        print("\n")
        print("-"*25 + "%s: 每日签到开始"%self.login_uid + "-"*25)
        playload = self.formData
        #得到xhr
        xhr = "xhr_" + str(int(time.time()*1000))
        playload["xhrPostKey"] = xhr
        #构建提交表单数据

        playload["iFlowId"] = self.type_dict["mrqd"][0]
        playload["param"] = self.type_dict["mrqd"][1]
        playload["iActivityId"] = self.type_dict["mrqd"][2]

        response = self.session.post(self.url_list[0],data=playload,headers=self.headers)
        self.print_msg(response)
        print("-"*25 + "%s: 每日签到结束"%self.login_uid + "-"*25)
        print("\n")


    def yinhaoLiCai(self):
        """
            银号理财
        """

        print("-"*25 + "%s: 银号理财开始"%self.login_uid + "-"*25)

        playload = self.formData
        #和其它3个任务的数据不一样,需要删除source,增加plat
        del playload["source"]
        playload["plat"] = "1"

        #得到xhr
        xhr = "xhr_" + str(int(time.time()*1000)+1000)
        playload["xhrPostKey"] = xhr
        #构建提交表单数据

        playload["iFlowId"] = self.type_dict["yhlc"][0]
        playload["param"] = self.type_dict["yhlc"][1]
        playload["iActivityId"] = self.type_dict["yhlc"][2]

        response = self.session.post(self.url_list[1],data=playload,headers=self.headers)

        self.print_msg(response)
        print("-"*25 + "%s: 银号理财结束"%self.login_uid + "-"*25)
        print("\n")

    def getCookie(self):
        """
            得到cookie,并把cookie添加到session
        """
        #print("-"*25 + "%s: 开始获取Cookie"%self.login_uid + "-"*25)
        driver = webdriver.Chrome(executable_path= self.chromePath)
        driver.get(self.loginUrl)
        #点击登录
        driver.execute_script("javascript:LoginManager.login(comm.app.login);")
        #切换到弹出来的iframe框架
        driver.switch_to_frame("loginIframe")
        #切换到帐号密码登录
        driver.find_element_by_id("switcher_plogin").click()
        #输入帐号
        driver.find_element_by_id("u").send_keys(self.login_uid)
        #输入密码
        driver.find_element_by_id("p").send_keys(self.login_pwd)
        #点击登录
        driver.find_element_by_id("login_button").click()
        #稍微延迟一下方便得到skey,不延迟在有些情况下得不到skey
        time.sleep(1)
        driver.get(self.loginUrl)
        time.sleep(1)

        cookies = driver.get_cookies()
        #退出driver
        driver.quit()
        time.sleep(1)
        skey = ""
        cookies_ = {}
        for cookie in cookies:
            if cookie['name'] == 'skey':
                #保存skey,需要计算g_tk
                skey = cookie['value']
                #print(skey)
            cookies_[cookie['name']] = cookie['value']
        requests.utils.add_dict_to_cookiejar(self.session.cookies,cookies_)
        #计算gtk,保存到playload
        if skey == "":
            print("-"*25 + "%s: cookies Could not find skey")
            sys.exit()
        g_tk = str(self.gtk(skey))
        self.formData["g_tk"] = g_tk
        #print("-"*25 + "%s: 获取Cookie结束"%self.login_uid + "-"*25)
    def huoquJiFen(self):
        """
            获取当前积分
        """
        #得到xhr
        playload = self.formData
        xhr = "xhr_" + str(int(time.time()*1000))
        #构建提交表单数据

        playload["xhrPostKey"] = xhr
        playload["iFlowId"] = self.type_dict["hqjf"][0]
        playload["iActivityId"] = self.type_dict["hqjf"][1]

        response = self.session.post(self.url_list[0],data=playload,headers=self.headers)
        #print(response.json())
        return int(response.json()["modRet"]["sOutValue1"])



    def gtk(self,skey):
        """
            计算gtk
        """
        
        #print("-"*25 + "%s: gtk start"%self.login_uid + "-"*25)
        e = 5381
        for i in range(len(skey)):
            e = e + (e<<5)+ord(skey[i])
        g_tk = str(2147483647 & e)
        #print("g_tk:%s"%g_tk)
        #print("-"*25 + "%s: gtk end"%self.login_uid + "-"*25)
        return g_tk

    def print_msg(self,response):
        """
            response.content是原始的二进制数据，json.loads()默认编码utf-8。
            json.dumps : dict转成str
            json.loads:str转成dict
            https://segmentfault.com/q/1010000004458927

            dicts = json.loads(response.content)
        """
        if response.encoding != 'utf-8':
            #print(response.encoding)
            response.encoding = 'utf-8'
        dicts = response.json()
        try:
            print(dicts["modRet"]["dTimeNow"])
            print(dicts["modRet"]["sMsg"])
        except KeyError:
            print(dicts["msg"])
            print(dicts["flowRet"]["sMsg"])


def start_work(login_uid,login_pwd):
    qiandao = QianDao(login_uid,login_pwd)
    qiandao.meiriQianDao()
    time.sleep(5)
    qiandao.fenxiangHaoYou()
    time.sleep(5)
    qiandao.fenxiangKongJian()
    time.sleep(5)
    qiandao.yinhaoLiCai()




if __name__ == '__main__':

    qq_list =  [
        ("100000","password"),
        ]
    pl = Pool(len(qq_list))

    for qq in qq_list:
        pl.apply_async(start_work,qq)


    print("*"*25 + "开始运行" + "*"*25)
    oldTime = time.time()
    print('开始时间 %f' % oldTime)
    pl.close()
    pl.join()
    currentTime = time.time()
    print('结束时间 %f' % currentTime)
    print('总运行时间 %f' % (currentTime - oldTime))
    print("*"*25 + "运行结束" + "*"*25)

