# ecology_oa_FileDownloadForOutDoc_sql.
泛微OA FileDownloadForOutDoc reception SQL inject 检测利用脚本



# 免责声明
使用本程序请自觉遵守当地法律法规，出现一切后果均与作者无关。

本工具旨在帮助企业快速定位漏洞修复漏洞,仅限授权安全测试使用!

严格遵守《中华人民共和国网络安全法》,禁止未授权非法攻击站点！

由于用户滥用造成的一切后果与作者无关。

切勿用于非法用途，非法使用造成的一切后果由自己承担，与作者无关。


### 食用方法

```
python .\ecology_oa_FileDownloadForOutDoc_sql.py -h
```

效果图

![image](https://github.com/FeiNiao/ecology_oa_FileDownloadForOutDoc_sql./assets/66779835/626987d3-52a9-4137-8231-bd9d09501986)

### 参数介绍
### 单url检测
```
python .\ecology_oa_FileDownloadForOutDoc_sql.py -u http://123.abc.com
```
效果图

![image](https://github.com/FeiNiao/ecology_oa_FileDownloadForOutDoc_sql./assets/66779835/c1161bf2-e85d-46a5-8601-fc6bcda06afd)


### 多url检测(txt文本形式)，最后疑似存在延时注入的url都会存储到当前目录下的`res.txt`中
```
python .\ecology_oa_FileDownloadForOutDoc_sql.py -f host.txt
```
效果图

![image](https://github.com/FeiNiao/ecology_oa_FileDownloadForOutDoc_sql./assets/66779835/66a40319-0af6-4ebc-808c-21d3dcf848ed)



### 遍历目标当前数据库名
```
python .\ecology_oa_FileDownloadForOutDoc_sql.py -u http://123.abc.co -db
```
效果图

![image](https://github.com/FeiNiao/ecology_oa_FileDownloadForOutDoc_sql./assets/66779835/d6024258-fdce-4e79-ad03-2d0dfb19c9a0)



### 遍历sysadmin用户的数据密文，此密文需要进行md5解密
```
python .\ecology_oa_FileDownloadForOutDoc_sql.py -u http://123.abc.com -e 
```

效果图

![image](https://github.com/FeiNiao/ecology_oa_FileDownloadForOutDoc_sql./assets/66779835/5fcfc72b-527a-4e84-b778-eda416856200)


Okay!

此脚本是根据https://github.com/izzz0 该作者进行学习改编而来，个人觉得代码规范很好，今后的代码也会按照这样的规范进行编写。Thanks！








