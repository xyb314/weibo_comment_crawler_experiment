import glob
import shutil
import os


wholeUsers = {}
with open('wholeCount.csv', 'r', encoding='utf-8') as f:
    temp = f.read().split('\n')
    for t in temp:
        if t == '':
            continue
        tt = t.split(',')
        wholeUsers.update({tt[0]: tt[1]})
dates = []
for file in glob.glob('*_count.csv'):
    dates.append(file.split('_')[0])
for d in dates:
    users = {}
    with open(d + '_count.csv', 'r', encoding='utf-8') as f:
        temp = f.read().split('\n')
        for t in temp:
            if t == '':
                continue
            tt = t.split(',')
            users.update({tt[0]: tt[1]})
    for file in glob.glob(d + '\\*.csv'):
        if '_extend' in file:
            continue
        output_text = ''
        with open(file, 'r', encoding='gbk') as f:
            temp = f.read().split('\n')
        for t in temp:
            if t == '':
                continue
            if t == 'User,Reter,Comment,Votes,Time':
                output_text += t + ',Count'
            else:
                user = t.split(',')[0]
                try:
                    output_text += '\n' + t + ',' + users[user]
                except Exception as e:
                    print(e, d, file)
        with open(file.replace('.csv', '_extend.csv'), 'w', encoding='gbk') as f:
            f.write(output_text)
            
            
for file in glob.glob('*\\*_extend.csv'):
    if not os.path.exists('extend\\' + file.split('\\')[0]):
        os.makedirs('extend\\' + file.split('\\')[0])
    shutil.copy(file, 'extend\\' + file.replace('_extend.csv', '.csv'))
