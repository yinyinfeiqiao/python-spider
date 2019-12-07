
```
使用多线程技术爬取1024xp图片栏目
失败重试
# http://a1.fkncjgdbb.xyz/pw/thread.php?fid=15
```

import os
import re
import socket
import threading
import traceback
import urllib
from urllib import error

import pymysql as pymysql


def  db_sql():
    db = pymysql.connect(host='localhost',
                         port=3306, # 端口号
                         user='root',
                         password='12345', # 密码
                         database='1024xp') # 数据库
    cursor = db.cursor() # 建立一个游标对象
    sql = """select *  from reveal where is_download is null and page < 501  limit 10""" # sql语句
    cursor.execute(sql)
    data = cursor.fetchall()
    # print ("Database version : %s " % data)
    # 关闭数据库连接
    db.close()
    print('连接数据库,取数据'+str(data))
    return data;


def  db_sql1(id):
    print('连接数据库，更新ID %s' % str(id))
    db = pymysql.connect(host='localhost',
                         port=3306, # 端口号
                         user='root',
                         password='12345', # 密码
                         database='1024xp') # 数据库
    cursor = db.cursor() # 建立一个游标对象
    sql = """update reveal set is_download = 1 where id = %s""" % id # sql语句
    cursor.execute(sql);
    db.commit()
    db.close()



headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
}

class download_thread(threading.Thread):
    def __init__(self, url,ti,path,index):
        threading.Thread.__init__(self)
        self.url=url
        self.ti=ti
        self.path=path
        self.index=index
    def run(self):
        print("thread %s" % self.index)
        j = 0
        while j<5:
            try:
                url=self.url;
                name=self.name;
                ti=self.ti;
                path=self.path;
                picname=url[url.rfind("/"):].split(".")[0];
                print("%s ,%s, Download : %s/%s.jpg" % (name,url ,ti.encode("utf-8"),picname ))
                # html = requests.get(url,headers=headers)
                req = urllib.request.Request(url,headers=headers)
                res = urllib.request.urlopen(req,timeout=10)
                image = res.read()
                with open(path + "/%s.jpg"%(picname.replace("*","")),"wb") as f:
                    f.write(image)
                break

            except Exception:
                print('str(Exception):\t', str(Exception))
                print('traceback.print_exc():%s' % traceback.print_exc())
                print('traceback.format_exc():\n%s' % traceback.format_exc());
                print('Unkown Error!')
                j+=1;
                continue;

def SavePath(urlList,page,title):
    savePath = "D:\\pic1\\%s\\%s" % (page ,title)
    savePath=savePath.replace("/"," ") \
        .replace("，"," ") \
        .replace("。"," ") \
        .replace("*"," ") \
        .replace("！"," ") \
        .replace("?"," ") \
        .replace("Hoteme:","") \
        .replace("白:","") \
        .replace("\""," ") \
        .replace("<", " ") \
        .replace(">", " ") \
        .replace("|", " ")
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    threads = []
    not_url=("s7tu.com/images/2017");
    for i in range(len(urlList)):
        print(i)
        if str(urlList[i]).find("p.usxpic.com") > 0:
            continue;
        if str(urlList[i]).find("snapgram.co") > 0 or str(urlList[i]).find("33img.com/upload/image/2017") > 0:
            continue
        if str(urlList[i]).find("img8.upoladhouse.com") > 0 or str(urlList[i]).find("niupiic.com") > 0 or str(urlList[i]).find("s7tu.com/images/2017") > 0 or str(urlList[i]).find("c.siimg.com/u/2017") > 0 or str(urlList[i]).find("v.siimg.com/u/2017") > 0 or str(urlList[i]).find("33img.com/u/2017") > 0 or str(urlList[i]).find("cdn4.snapgram.co") > 0:
            continue
        # p=False;
        # for j in range(len(not_url)):
        #     if(str(urlList[i]).find(not_url[j]) > 0):
        #         p=True;
        #         break;
        # if p:
        #     continue;
        #
        # print(p)


        thread= download_thread(urlList[i],title,savePath,"thread-"+str(i))
        thread.start();
        threads.append(thread)
    for thread in threads:
        thread.join()


def downloadImg(url,title,path,name):
    print(name)

def worker(url,p,t,id):
    k=0;
    while k<5:
        try: #使用try except方法进行各种异常处理
            print("http://a.cnjdmm.rocks/pw/"+url)
            req1 = urllib.request.Request(url="http://a.cnjdmm.rocks/pw/"+url, headers=headers)
            page1  = urllib.request.urlopen(req1,timeout=5);
            html1=page1.read()
            print(html1)
            # part_picURL =
            pattern1 = re.compile(r'src="([.*\S]*\.jpg)" border="0"')
            item_list1 = pattern1.findall(html1.decode("utf-8"),re.S)
            SavePath(item_list1,'page'+str(p),t)
            db_sql1(id);
            break;
        except error.HTTPError as err:
            print('HTTPerror, code: %s' % err.code)
            k+=1;
            continue;
        except error.URLError as err:
            print('URLerror, reason: %s' % err.reason)
            k+=1;
            continue;
        except socket.timeout:
            print('Time Out!')
            k+=1;
            continue;
        except Exception:
            print('str(Exception):\t', str(Exception))
            print('traceback.print_exc():%s' % traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc());
            print('Unkown Error!')
            k+=1;
            continue;

if __name__ == '__main__':
    while 1:
        item=db_sql()
        print(item)

        main_thread=[];
        for i in range(0,10):
            t = threading.Thread(target=worker, args=(item[i][3],item[i][1],item[i][2],item[i][0]) )
            t.start();
            main_thread.append(t);
        for thread in main_thread:
            thread.join();
        # t1 = threading.Thread(target=worker, args=(item[0][3],item[0][1],item[0][2],item[0][0]) )
        # t2 = threading.Thread(target=worker, args=(item[1][3],item[1][1],item[1][2],item[1][0]) )
        # t3 = threading.Thread(target=worker, args=(item[2][3],item[2][1],item[2][2],item[2][0]) )
        # t4 = threading.Thread(target=worker, args=(item[3][3],item[3][1],item[3][2],item[3][0]) )
        # t5 = threading.Thread(target=worker, args=(item[4][3],item[4][1],item[4][2],item[4][0]) )
        # t6 = threading.Thread(target=worker, args=(item[5][3],item[5][1],item[5][2],item[5][0]) )
        # t7 = threading.Thread(target=worker, args=(item[6][3],item[6][1],item[6][2],item[6][0]) )
        # t8 = threading.Thread(target=worker, args=(item[7][3],item[7][1],item[7][2],item[7][0]) )
        # t9 = threading.Thread(target=worker, args=(item[8][3],item[8][1],item[8][2],item[8][0]) )
        # t10 = threading.Thread(target=worker, args=(item[9][3],item[9][1],item[9][2],item[9][0]) )
        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        # t5.start()
        # t6.start()
        # t7.start()
        # t8.start()
        # t9.start()
        # t10.start()
        # t1.join();
        # t2.join();
        # t3.join()
        # t4.join()
        # t5.join()
        # t6.join();
        # t7.join();
        # t8.join()
        # t9.join()
        # t10.join()

