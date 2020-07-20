from bs4 import BeautifulSoup
import requests
import re
import xlwt

class QiShunWang:
    def __init__(self):
        self.URL=''
        self.header = {          #消息头，伪装成浏览器访问
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
     #   self.header={'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    def GetPage(self):
        html=requests.get(self.URL,params='pn2',headers=self.header)    #request包发出请求
        soup=BeautifulSoup(html.text,"html.parser")                     #htmp.parser是常用的HTML解析
        page=[]                                                         #用一个类链表存储符合要求的数据
        for i in range(1,101):
            temp=ADiv()
            money=soup.select('#il > div:nth-child(2) > div > ul > li:nth-child('+str(i)+') > div.f_l > span:nth-child(4)')  #找到要抓取的地方右键-检查-右键-copy-copyslector即可
            for m in money:   #想要抽取text，这个循环是必要的，虽然只有一个值
                temp.money = m.get_text()
            if(temp.MoneyJudge()):
                address = soup.select('#il > div:nth-child(2) > div > ul > li:nth-child(' + str(i) + ') > div.f_l > div:nth-child(3)')
                name = soup.select('#il > div:nth-child(2) > div > ul > li:nth-child(' + str(i) + ') > div.f_l > h4 > a')
                for n in name:
                    temp.name = n.get_text()
                url=n.attrs['href']
                html_2 = requests.get('http:'+url,params='', headers=self.header)
                soup_2 = BeautifulSoup(html_2.text, "html.parser")
                manager=soup_2.select('#contact > div > dl > dd:nth-child(6)')
                phone=soup_2.select('#contact > div > dl > dd:nth-child(8)')
                tel=soup_2.select('#contact > div > dl > dd:nth-child(4)')
                for a in address:
                    temp.address = a.get_text()
                for man in manager:
                    temp.manager=man.get_text()
                for p in phone:
                    temp.phone=p.get_text()
                for t in tel:
                    temp.tel=t.get_text()
                print(str(n))
                page.append(temp)
        return page






class ADiv:
    def __init__(self):
        self.name=''
        self.address=''
        self.money=''
        self.manager=''
        self.phone=''
        self.tel=''
    def MoneyJudge(self):        #返回布尔值，判断注册资本是否大于100万
        num=re.findall('\d+',self.money)

        if num :
            num = int(num[0])
            if (num > 100) or (num == 100):
                return True
            else:
                return False
        else:
            return False


def WriteToExcel(page,hang,worksheet,workbook):

    for tem in page:
        worksheet.write(hang,0,str(tem.name))
        worksheet.write(hang, 1, str(tem.money))
        worksheet.write(hang, 2, str(tem.manager))
        worksheet.write(hang, 3, str(tem.phone))
        worksheet.write(hang, 4, str(tem.tel))
        worksheet.write(hang, 5, str(tem.address))
        hang=hang+1
    # 保存
    workbook.save('Excel_test.xls')

    print('成功写入')
    return hang

if __name__ == '__main__':
    hang=0
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('My Worksheet')
    for i in range(1,21):
       cls=QiShunWang()
       if i==1:
           cls.URL='http://chengdu.11467.com/wuhou/huochenanzhanjiedao/'
       else:
           cls.URL='http://chengdu.11467.com/wuhou/huochenanzhanjiedao/'+'pn'+str(i)
       page=cls.GetPage()
       hang=WriteToExcel(page,hang,worksheet,workbook)
