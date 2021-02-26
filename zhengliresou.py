import re
import csv
import os
import glob

# 解析网页结构
def parse_page(html):
    info = []
    patten1 = re.compile(r'<span class="card-num">(.*?)</span>(.*?)</h3>'
                         r'.*?搜索量 (.*?)</p>.*?当日累计在榜时间：(.*?)</p>'
                         r'.*?当日最高排名.*?<strong>(.*?)</strong>', re.S)
    datas1 = re.findall(patten1,str(html))
    for data in datas1:
        comic = {}
        comic['InfoID'] = data[0].strip()
        comic['Title'] = data[1].strip()
        comic['Search'] = data[2].strip()
        comic['OnTime'] = data[3].strip()
        comic['HiRank'] = data[4].strip()
        comic['Link'] = ''
        info.append(comic)
    return info

# 保存数据
def write_csv(filetitle,info):
    with open(filetitle+'.csv', 'a', newline='') as f:
        fieldnames = ['InfoID', 'Title', 'Search', 'OnTime', 'HiRank','Link']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(info)
        except:
            pass

# 主函数
def main():
    for afile in glob.glob('*'):
        dot_situation = afile.rfind('.')
        filetitle = afile[0:dot_situation]
        filetype = afile[dot_situation:]
        if filetype == '.txt':
            f = open(afile,encoding='utf-8')
            html = f.read()
            info = parse_page(html)
            write_csv(filetitle,info)
        else:
            continue

if __name__ == '__main__':
    main()