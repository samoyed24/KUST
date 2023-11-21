import pandas as pd
import openpyxl, json, time

def lsget(ls, idx, dft=''):
    if(idx+1>len(ls)):
        return dft
    return removefh(ls[idx])

def removefh(s):
    if s[-1] == ';':
        return s[:-1]
    else:
        return s

def letterplus(s):
    return chr(ord(s)+1)

wkdaydict = {
    '周一' : 'B',
    '周二' : 'D',
    '周三' : 'F',
    '周四' : 'H',
    '周五' : 'J',
    '周六' : 'L',
    '周日' : 'N'
}

lsdict = {
    '第一节' : '3',
    '第三节' : '5',
    '第六节' : '8',
    '第九节' : '11',
    '第十一节' : '13',
}

dfdatadict = {
    '课程代号':[],
    '课程名称':[],
    '周数':[],
    '星期':[],
    '起节':[],
    '终节':[],
    '校区':[],
    '地点':[],
}

def genTable(tabledata, username):
    templatepath = 'table_template.xlsx'
    wb=openpyxl.load_workbook(templatepath)
    table=wb['Sheet1']

    # with open('timetable.json', 'r', encoding='utf-8') as f:
    #     tabledata  = json.load(f)
    lessons = tabledata['lessons']
    for lesson in lessons:
        code = lesson['code']
        name = lesson['course']['nameZh']
        Linfo = lesson['scheduleText']['dateTimePlaceText']['text']
        if(type(Linfo) == str):
            difblock = [s.strip().split(' ') for s in Linfo.split('\n')]
            for block in difblock:
                dfdatadict['课程名称'].append(name)
                dfdatadict['课程代号'].append(code)
                dfdatadict['周数'].append(lsget(block, 0))
                dfdatadict['星期'].append(lsget(block, 1))
                ft = lsget(block, 2)
                if(ft):
                    ftlist = ft.split('~')
                    dfdatadict['起节'].append(ftlist[0])
                    dfdatadict['终节'].append(ftlist[1])
                else:
                    dfdatadict['起节'].append('')
                    dfdatadict['终节'].append('')
                dfdatadict['校区'].append(lsget(block, 3))
                dfdatadict['地点'].append(lsget(block, 4))

    df = pd.DataFrame(data=dfdatadict)

    for s in df.itertuples():
        wkday = wkdaydict[s[4]]
        start = lsdict[s[5]]
        info = f'{s[1]}\n{s[2]}\n{s[3]}\n{s[5]}~{s[6]}\n{s[7]} {s[8]}'
        loc = f'{wkday}{start}'
        if table[loc].value:
            table[loc].value = '\n'+info
        else:
            table[loc].value = info
    curtime = time.strftime('%Y-%m-%d', time.localtime())
    filename = f'{curtime}_{username}_Timetable.xlsx'
    wb.save(filename)
    print('课表获取成功,已保存至', filename)