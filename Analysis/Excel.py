import xlrd
import xlwt
import xlutils
import mysql.connector


def opens_read():
    # 打开一个文件
    book = xlrd.open_workbook('./old/中牟店.xls')
    # 表单数量
    print(book.nsheets)
    # 表单名
    print(book.sheet_names())
    # 获取第x个表单，索引从0开始
    sh = book.sheet_by_index(1)
    print(type(sh))
    # 表单名，表单行数，表单列数
    print(sh.name, sh.nrows, sh.ncols)
    # 返回sheet的第5行，第4列
    print(sh.cell_value(4, 3))
    for s in book.sheets():
        print(s.name)
        for r in range(s.nrows):
            print(s.row(r))


def opens_write():
    # 创建xls文件对象
    wb = xlwt.Workbook()
    # 添加一个sheet
    ws = wb.add_sheet('第一个测试')
    # 在指定位置写入数据
    ws.write(0, 0, '姓名')
    ws.write(1, 0, '赵翔鹏')
    ws.write(2, 0, '时蕊')
    ws.write(0, 1, '生日')
    ws.write(1, 1, '八月十七')
    ws.write(2, 1, '十月一日')
    # 保存文件
    wb.save('./birthday.xls')


def open_revise():
    op = xlrd.open_workbook('./birthday.xls')
    se = op.get_sheet(0)
    se.write()

if __name__ == '__main__':
    opens_write()
    print('SUCCESS')
    pass