# SSR机场自动签到脚本（自动领取流量）

## Notice
> + 支持 `Python3`
> + 目前只支持 `SSPANEL`机场
> + 目前不支持带有验证码的机场
> + 支持设置多个服务器，并寻找延迟最低的服务器

## Install
+ 1.下载本库
+ 2.安装依赖库
```shell
pip3 install -U requests
```
+ 3.修改 `SConfig.json` 配置文件
```json
{
    "retry": 2,
    "site": [
        {
            "note": "机场1", //备注
            "url": [
                "https://a.com",
                "https://aa.net"
            ], //机场服务器，末位不可为'/'，多个追加
            "email": "123@qq.com",//登录邮箱
            "password": "1111",//登录密码
            "cookies": ""//cookies如账号密码无误可不设置，会自动获取
        },
        {
            "note": "机场2",//备注
            "url": [
                "https://b.com",
                "https://bb.net"
            ],//机场服务器，末位不可为'/'，多个追加
            "email": "123@qq.com",//登录邮箱
            "password": "1111",//登录密码
            "cookies": ""//cookies如账号密码无误可不设置，会自动获取
        }//单个机场删掉此对象
    ]
}
```
## Usage
### 青龙
+ 1.将`airport.py`、`SConfig.json`放到`scripts`文件夹内(如无`sendNotify.py`也请放入)
+ 2.添加任务。名称`机场签到`命令`task airport.py`定时规则`0 30 7 * * ?`
### 其他
+ `windows` 操作系统可通过 `任务计划程序` 添加到定时任务，详细百度
+ `Linux` 或 `MacOS` 可通过 `cron` 添加到定时任务（或登陆启动项），详细百度
