import xlrd
import xlwt
import xlutils
import shutil
import os

path1 = './data2/'
path2 = './ok/'
path3 = './error/'

def paths():
    Path = path1
    for names in os.walk(Path):
        # print(names)
        for file in names[2]:
            judge(file)


def judge(file):
    # 打开一个文件
    book = xlrd.open_workbook('./data2/{0}'.format(file))
    # 表单数量
    # print(book.nsheets)
    # 获取第x个表单，索引从0开始
    sh = book.sheet_by_index(0)
    # print(type(sh))
    # 表单名，表单行数，表单列数
    print(file, sh.nrows)
    if sh.nrows == 366:
        shutil.copy('./data2/{0}'.format(file), path2)
    else:
        shutil.copy('./data2/{0}'.format(file), path3)


paths()