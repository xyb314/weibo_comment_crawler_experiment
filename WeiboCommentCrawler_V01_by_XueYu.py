import requests
from urllib.parse import urlencode
import re
import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# 获取网页请求数据
def get_data(title,num,base_url):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

    url = base_url + '&page=' + str(num)
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    print(time_str+'  正在采集话题《'+title+'》第'+str(num)+'页:'+ url)
    time.sleep(3)
    driver.get(url)
    cookies = driver.get_cookies()
    cookies_dict={}
    cookie_text=''
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
    for key,value in cookies_dict.items():
        cookie_text = cookie_text + '{key}={value}; '.format(key=key,value=value)
    cookie_text = cookie_text.rstrip('; ')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Host':'weibo.cn',
        'Accept': 'application/json,text/plain,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip,deflate,br',
        'Cookie': cookie_text,
        'DNT': '1',
        'Connection': 'keep-alive'
    }
    tries = 1
    while(tries<4):
        try:
            response = requests.get(url, headers = headers, verify = False, timeout=5)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            print(time_str+'  Error for '+str(tries)+' time(s).',end='    ')
            print(e)
            tries += 1
            if tries >3:
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                print(time_str+'  话题《'+title+'》第'+str(num)+'页评论爬取失败，请手动检查！')
                return None

# 解析网页结构
def parse_page(html):
    info = []
    curr_time = datetime.datetime.now()
    patten1 = re.compile(r'<div class="c" id=".*?<a href=".*?">(.*?)</a'
                         r'.*?<span class="ctt">(.*?)</span>.*?赞[?=\\[](.*?)]</a'
                         r'.*?<span class="ct">(.*?)&nbsp;', re.S)
    patten2 = re.compile(r'回复.*?>@(.*?)</a>:(.*?)dd',re.S)
    patten3 = re.compile(r'<.*?>',re.S)
    datas1 = re.findall(patten1,str(html))
    for data in datas1:
        comic = {}
        comic['Comment'] = data[1].strip().replace('\n', ' ')
        if comic['Comment'] == '':
            continue
        comic['User'] = '@'+data[0].strip()
        comic['Reter'] = ''
        if re.match('回复', comic['Comment'])!=None:
            ttmp=comic['Comment']+'dd'
            datas2 = re.findall(patten2,ttmp)
            for doto in datas2:
                comic['Reter'] = '@'+doto[0].strip()
                comic['Comment'] = doto[1].strip().replace('\n',' ')
        datas3 = re.findall(patten3,comic['Comment'])
        for dutu in datas3:
            ttcomment = comic['Comment'].replace(dutu,'')
            comic['Comment']=ttcomment
        comic['Comment'] = comic['Comment'].strip(':')
        comic['Votes'] = data[2].strip()
        comic['Time'] = data[3].strip()
        if re.match('今天',comic['Time'])!=None:
            ttime=comic['Time'].replace('今天',curr_time.strftime('%y-%m-%d'))
            comic['Time']=ttime
        if re.match('.*?月.*?日',comic['Time'])!=None:
            ttime=str(curr_time.year)+'-'+comic['Time'].replace('月','-').replace('日','')
            comic['Time'] = ttime
        if re.match('.*?分钟前',comic['Time'])!=None:
            tminutes=re.findall('(.*?)分钟前',comic['Time'])
            ttime=(curr_time+datetime.timedelta(minutes=int(tminutes[0]))).strftime('%y-%m-%d %H:%M')
            comic['Time']=ttime
        info.append(comic)
    if info != []:
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
        print(time_str+'  Success!')
        return info
    else:
        return 'Nothing'

# 保存数据
def write_csv(num,info,title,topic_file_name):
    with open(topic_file_name+'/'+title+'.csv', 'a', newline='') as f:
        fieldnames = ['User', 'Reter', 'Comment', 'Votes', 'Time']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if num == 1:
            writer.writeheader()
        try:
            writer.writerows(info)
        except:
            pass

# 主函数
def main():
    topic_file_names=open('dateconfig.txt','r').read().split('\n')
    if '' in topic_file_names:
        topic_file_names.remove('')
    for topic_file_name in topic_file_names:
        with open(topic_file_name+'.csv','r+') as f:
            if os.path.exists(topic_file_name)!=True:
                os.mkdir(topic_file_name)
            text = csv.reader(f)
            rows = [row for row in text]
            nrow = len(rows)
            for ii in range(1,nrow):
                title = rows[ii][1] #input('请输入话题:')
                base_url = rows[ii][5] #input('请输入链接:')
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                print(time_str+'  开始话题《'+title+'》的爬取！')
                last_info = []
                for num in range(1,50,1):
                    html = get_data(title,num, base_url)
                    info = parse_page(html)
                    if info == 'Nothing':
                        continue
                    if info == last_info:
                        curr_time = datetime.datetime.now()
                        time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                        print(time_str+'  结束话题《'+title+'》的爬取！')
                        break
                    write_csv(num,info,title,topic_file_name)
                    last_info = info
                    if int(num)%10 == 0:
                        time.sleep(0)
                    if num == 50:
                        curr_time = datetime.datetime.now()
                        time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                        print(time_str+'  结束话题《' + title + '》的爬取！')

if __name__ == '__main__':
    print('\n****************************************************************\n')
    print('    WeiBo Comment Crawler ver.0.1 @ XueYu')
    print('    Connect XueYu by QQ:664020056 if having any questions!')
    print('\n****************************************************************\n')
    main()
    os.system('pause')