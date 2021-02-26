import glob

for file in glob.glob('*\\*.csv'):
    with open(file, 'r', encoding='gbk') as f:
        txt = f.read().split('\n')
        del txt[0]
    for i in range(len(txt)):
        temp = txt[i].split(',')
        temp[0] = ''
        temp[1] = ''
        temp[2] = ''
        temp[4] = ''
        txt[i] = ','.join(temp)
    with open(file, 'w', encoding='gbk') as f:
        f.write('\n'.join(txt))
