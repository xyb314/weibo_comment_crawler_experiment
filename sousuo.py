from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import datetime


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
cod_num=[]

for numnum in cod_num:
    with open(numnum+'.csv','r+') as f:
        text = csv.reader(f)
        rows = [row for row in text]
        nrow = len(rows)
        tt = ','.join(rows[0])
        f.seek(0)
        f.truncate()
        f.writelines(tt+'\n')
        for i in range(1,nrow):
            driver.get('https://weibo.cn/search/')
            try:
                driver.find_element_by_name('keyword').send_keys(rows[i][1])
                driver.find_element_by_name('smblog').click()
                driver.find_element_by_class_name('cc').click()
                driver.find_element_by_link_text('查看更多热门>>').click()
            except:
                continue
            rows[i][5] = driver.current_url
            new_text=','.join(rows[i])
            f.writelines(new_text+'\n')
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            print(time_str+'  '+numnum+'  '+str(i)+'/'+str(nrow-1))


