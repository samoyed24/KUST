from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame()

with open('test4.htm', 'r', encoding='utf-8') as f:
    text = f.read()
soup3 = BeautifulSoup(text, 'html.parser')

datadict = {
    '学期':[],
    '课程名称':[],
    '课程代码':[],
    '课程类别1':[],
    '课程类别2':[],
    '教学班代码':[],
    '成绩':[],
    '学分':[],
    '绩点':[],
    '学分绩点':[],
    '修读性质':[],
    '备注':[]
}

gradeinfo = soup3.find_all('div',{'class':'row'})
for gradeblock in gradeinfo:
    sem = gradeblock.find_all('div', {'class':'col-sm-12'})
    semname = sem[0].h3.text
    gradetb = sem[1]
    grades = gradetb.table.tbody.select('tr')
    for grade in grades:
        data = grade.select('td')
        datadict['学期'].append(semname)
        datadict['课程名称'].append(data[0].text.strip())
        datadict['课程代码'].append(data[1].text)
        datadict['课程类别1'].append(data[2].text)
        datadict['课程类别2'].append(data[3].text)
        datadict['教学班代码'].append(data[4].text)
        datadict['成绩'].append(data[5].text)
        datadict['学分'].append(data[6].text)
        datadict['绩点'].append(data[7].text)
        datadict['学分绩点'].append(data[8].text)
        datadict['修读性质'].append(data[9].text)
        datadict['备注'].append(data[10].text)

df = pd.DataFrame(data=datadict)
df.to_excel('课表.xlsx')