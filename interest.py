from flask import Flask

import requests
from bs4 import BeautifulSoup
import csv
import datetime

app = Flask(__name__)

@app.route('/hello/')
def hello():
    return "Hello World"

@app.route('/interest/<int:num>', methods=['GET'])
def get_interest(num):

    stock_list = []

    with open('list.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            stock_list = row

    now = datetime.datetime.now()
    this_year = now.year
    tw_year = now.year - 1911

    result = ''
    for i in range(10):
        year = tw_year - i
        query_string = "encodeURIComponent=1&step=1&firstin=1&off=1&keyword4=&code1=&TYPEK2=&checkbtn=&queryName=co_id&inpuType=co_id&TYPEK=all&isnew=false&co_id="+str(num)+"&year="+str(year)
        r = requests.post('http://mops.twse.com.tw/mops/web/ajax_t05st09', query_string)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.find('tr', class_='odd') is not None :
                tds = soup.find('tr', class_='odd').findAll('td')
                result += '年份：' + str(year) + ' 配息：' + tds[7].text + ' 配股：' + tds[10].text + '\n'

    return result

if __name__== '__main__' :
    app.run()
