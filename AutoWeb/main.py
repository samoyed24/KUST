import requests, time
from bs4 import BeautifulSoup
from rsatest import RSA
import pandas as pd
import tablegen

username=input('学号:')
password=RSA(input('密码:'))

s = requests.Session()
r = s.get('https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fjwctsp.kmust.edu.cn%2Fintegration%2Fkcas-sso%2Flogin')
r.encoding = 'utf8'
soup1 = BeautifulSoup(r.text, 'html.parser')
lt = soup1.find('input', {"name":"lt"}).attrs['value']
execution = soup1.find('input', {"name":"execution"}).attrs['value']
_eventId = soup1.find('input', {"name":"_eventId"}).attrs['value']

data = {
    'username':username,
    'password':password,
    'captcha':'',
    'warn':True,
    'lt':lt,
    'execution':execution,
    '_eventId':_eventId
}

# print(data)
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
s.post('https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fjwctsp.kmust.edu.cn%2Fintegration%2Fkcas-sso%2Flogin', data=data, headers=headers)
s.get('https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fjwctsp.kmust.edu.cn%2Fintegration%2Fkcas-sso%2Flogin', headers=headers)

r = s.get('http://jwctsp.kmust.edu.cn/integration/for-std/best/grade/sheet')
r.encoding = 'utf-8'
soup2 = BeautifulSoup(r.text, 'html.parser')
studentid = soup2.find('form',{'target':'student-grades'}).attrs['action'].split('/')[-1]
r = s.get(f'http://jwctsp.kmust.edu.cn/integration/for-std/best/grade/sheet/info/{studentid}?semester=')
#print(r.text) #调试用
with open('test4.htm', 'w', encoding='utf-8') as f:
    f.write(r.text)
soup3 = BeautifulSoup(r.text, 'html.parser')

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
curtime = time.strftime('%Y-%m-%d', time.localtime())
df = pd.DataFrame(data=datadict)
filename = f'{curtime}_{username}_GradeReport.xlsx'
df.to_excel(filename)
print('成绩单获取成功,已保存至', filename)
r = s.get('http://jwctsp.kmust.edu.cn/integration/for-std/course-table/get-data?bizTypeId=2&semesterId=282')
tablegen.genTable(r.json(), username)