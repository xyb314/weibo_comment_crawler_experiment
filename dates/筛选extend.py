import glob
import shutil
import os

for file in glob.glob('*\\*_extend.csv'):
    if not os.path.exists('extend\\' + file.split('\\')[0]):
        os.makedirs('extend\\' + file.split('\\')[0])
    shutil.copy(file, 'extend\\' + file.replace('_extend.csv', '.csv'))
