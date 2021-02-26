import glob


wholeUsers = {}
for csvFile in glob.glob('*.csv'):
    title = csvFile.replace('.csv', '')
    users = {}
    for file in glob.glob(title + '\\*.csv'):
        with open(file, 'r', encoding='gbk') as f:
            blogs = f.read().split('\n')
            for i in range(1, len(blogs)):
                user = blogs[i].split(',')[0]
                if user not in users.keys():
                    users.update({user: 0})
                users.update({user: users[user] + 1})
    output_text = ''
    for user in users.keys():
        output_text += user + ',' + str(users[user]) + '\n'
    with open(title + '_count.csv', 'w', encoding='utf-8') as f:
        f.write(output_text)
    wholeUsers.update(users)

output_text = ''
for user in wholeUsers.keys():
    output_text += user + ',' + str(wholeUsers[user]) + '\n'
with open('wholeCount.csv', 'w', encoding='utf-8') as f:
    f.write(output_text)

'''
count = 0
for csvFile in glob.glob('*.csv'):
    title = csvFile.replace('.csv', '')
    count += len(glob.glob(title + '\\*.csv'))
print(count)
'''