import pandas as pd
import openpyxl


def T1():
    # 待拆分的Excel文件位置
    file = './data/客户科目明细账.XLS'
    # 拆分后的文件存放位置
    result = './data'
    # 读取待拆分的Excel文件
    df = pd.read_excel(file)
    # 获取拆分条件：去重
    jg_list = df['客户名称'].unique()
    # 按拆分条件分别保存新的Excel文件
    for jg in jg_list:
        child_wb = df[df['客户名称'] == jg]
        child_wb.to_excel(result + jg + '.xls', index=False)
    print('拆分完成！')


def T2():
    df = pd.read_excel('./data/发货单列表.XLS')
    df2 = df[df.duplicated('客户简称') == False]['客户简称']
    for i in df2:
        df3 = df[df['客户简称'] == i]
        df3.to_excel('./data2/{0}/发货单列表.xls'.format(i))


def T3_1():
    df = pd.read_excel('./data/发货单列表.XLS')
    df2 = df[df.duplicated('客户简称') == False]['客户简称']
    for i in df2:
        df3 = df[df['客户简称'] == i]
        df3.to_excel('./data2/{0}发货单列表.xls'.format(i))


def T3_2():
    df = pd.read_excel('./data/客户科目明细账.XLS')
    df2 = df[df.duplicated('客户名称') == False]['客户名称']
    for i in df2:
        df3 = df[df['客户名称'] == i]
        df3.to_excel('./data2/{0}客户科目明细账.xls'.format(i))


def T3_3():
    df = pd.read_excel('./data/应打款金额.XLS')
    df2 = df[df.duplicated('客户名称') == False]['客户名称']
    for i in df2:
        df3 = df[df['客户名称'] == i]
        df3.to_excel('./data2/{0}应打款金额.xls'.format(i))


def history():
    df = pd.read_csv('./data/Xiapid.csv')
    df2 = df[df.duplicated('大类别') == False]['大类别']
    for i in df2:
        df3 = df[df['大类别'] == i]
        try:
            df3.to_excel('D:\Code\Python_T\Analysis\data2\{0}.xls'.format(i), index=False)
        except:
            print(i)


if __name__ == '__main__':
    # T3_1()
    # T3_2()
    # T3_3()
    history()
    print('SUCCESS')