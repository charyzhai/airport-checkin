import re
import time
import requests
import json
import subprocess
import sendNotify
import platform


def GetQuery(U, C):
    try:
        url = U + "/user"
        payload = ''
        headers = {
            'Cookie': C,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            time.sleep(1)
            GetQuery(U, C)
        D = response.text.encode('utf8').decode('utf8')
        # print(D)
        if D.count("马上注册") > 0 or D.count("还没有账号") > 0 or D.count("登录失败") > 0:
            return '-1'
        pat = re.compile('<span class="counter">' + '(.*?)' + '</span>', re.S)
        result = pat.findall(D)
        pat1 = re.compile('<li class="breadcrumb-item active" aria-current="page">' + '(.*?)' + '</li>', re.S)
        result1 = pat1.findall(D)
        pat2 = re.compile('<span class="counterup">' + '(.*?)' + '</span>', re.S)
        result2 = pat2.findall(D)
        pat3 = re.compile(result[1] + '</span>' + '(.*?)' + '</div>', re.S)
        result3 = pat3.findall(D)
        pat4 = re.compile('<title>' + '(.*?)' + '</title>', re.S)
        result4 = pat4.findall(D)
        # print(result)
        # print(result1)
        '''
        if D.count("明日再来") == 2:
            feedback = '会员时长:已经签到' + "\r\n"
        else:
            feedback = '会员时长:未签到' + "\r\n"
        '''
        feedback = "机场：" + str(result4[0]).replace("&mdash;", "").replace("首页", "").replace(" ", "") + "\r\n"
        feedback = feedback + '会员时长:' + result[0] + "天\r\n"
        feedback = feedback + str(result1[0]).replace(
            '<a href="#" onclick="return_c()" class="btn btn-icon icon-left btn-primary">升级套餐</a>', "").replace(" ",
                                                                                                                "").replace(
            "\n", "").replace("\r", "") + "\r\n"
        feedback = feedback + '剩余流量:' + result[1] + str(result3[0]).replace(" ", "").replace("\n", "").replace("\r",
                                                                                                               "") + "\r\n"
        feedback = feedback + result1[1] + "\r\n"
        feedback = feedback + '在线设备数:' + result[2] + "/" + result2[0] + "\r\n"
        feedback = feedback + result1[2] + "\r\n"
        feedback = feedback + '钱包余额:' + result[3] + "\r\n"
        feedback = feedback + result1[3] + "\r\n"
        return feedback
    except BaseException as e:
        time.sleep(1)
        return GetQuery(U, C)


def SignIn(U, C):
    try:
        url = U + "/user/checkin"
        payload = ''
        headers = {
            'Cookie': C,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            time.sleep(1)
            SignIn(U, C)
        D = response.text.encode('ascii').decode('unicode_escape')
        J = json.loads(D)
        return J['msg']
    except BaseException as e:
        time.sleep(1)
        return SignIn(U, C)


def login(U, A, P):
    try:
        cookies = ''
        url = U + "/auth/login"
        payload = f'email={A}&passwd={P}&code='
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            time.sleep(1)
            login(U, A, P)
        for cookie in response.cookies:
            cookies = cookies + cookie.name + "=" + cookie.value + "; "
        D = response.text.encode('ascii').decode('unicode_escape')
        # {"ret":1,"msg":"登录成功"}
        J = json.loads(D)
        if J["msg"] != "登录成功":
            return J["msg"]
        else:
            return cookies
        # encode = chardet.detect(D)
        # print(encode['encoding'], D)
    except BaseException as e:
        time.sleep(1)
        return login(U, A, P)


def Ping(host):
    if platform.system() == 'Windows':
        try:
            ping = subprocess.Popen(["ping", host, "-n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)
            ping.wait()
            lines = ping.stdout.readlines()
            D = str([line.decode('gbk') for line in lines])
            pat = re.compile('平均' + '(.*?)' + 'ms', re.S)
            result = pat.findall(D)
            return str(result[0]).replace(" ", "").replace("=", "")
            # 数据包: 已发送 = 1，已接收 = 0，丢失 = 1 (100% 丢失)，\r\n
        except BaseException as e:
            return -1
    elif platform.system() == 'Linux':
        try:
            p = subprocess.Popen(
                "ping -c 1 {0} \n".format(host),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
            out = p.stdout.read().decode('gbk')
            pat = re.compile('time=' + '(.*?)' + ' ms', re.S)
            result = pat.findall(out)
            return result[0]
        except BaseException as e:
            return -1


def Account():
    with open('SConfig.json', 'r') as f:
        j = json.load(f)
    Feedback = '共计' + str(len(j['site'])) + "个站点需签到" + "\r\n" + "\r\n"
    for v in j['site']:
        url = ''
        print("开始计算最快的服务器。。。")
        U = [{}] * len(v['url'])
        for i, vv in enumerate(v['url']):
            ms = Ping(str(vv).replace("http://", "").replace("https://", ""))
            U[i] = {"ms": f'{ms}', "url": vv}
        U.sort(key=lambda x: x["ms"])
        # print(U)
        for vv in U:
            if vv['ms'] != "-1":
                url = vv['url']
                break
        print("最快的服务器为：" + url)
        # url = 'https://suying688.com'
        Cookies = v['cookies']
        if Cookies == "":
            #print(v)
            Cookies = login(url, v['email'], v['password'])
            if Cookies.count("=") > 0:
                v['cookies'] = Cookies
            else:
                Feedback = Feedback + "登录错误:" + Cookies + "\r\n"
        else:
            if GetQuery(url, Cookies) == "-1":
                Cookies = login(url, v['email'], v['password'])
                if Cookies.count("=") > 0:
                    v['cookies'] = Cookies
                else:
                    Feedback = Feedback + "登录错误:" + Cookies + "\r\n"
            case = SignIn(url, Cookies)
            Feedback = Feedback + "签到情况：" + case + "\r\n"
            case = GetQuery(url, Cookies)
            Feedback = Feedback + case + "\r\n" + "\r\n"
    with open('SConfig.json', 'w') as f:
        json.dump(j, f, indent=4)
    print(Feedback)
    sendNotify.send("机场签到通知", Feedback)


def main():
    Account()


if __name__ == '__main__':
    main()
