# --*-- coding : utf-8 --*--
# --*-- author : silly rabbit --*--

import requests
from bs4 import BeautifulSoup

class Douban:
    def __init__(self):
       self.URL = 'https://movie.douban.com/top250'
       self.starnum =[]
       for start_num in range(0,251,25):
           self.starnum.append(start_num)
       self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    def get_top250(self):
        for start in self.starnum:
            start = str(start)
            html = requests.get(self.URL, params={'start':start},headers = self.header)
            soup = BeautifulSoup(html.text,"html.parser")
            name = soup.select('#content > div > div.article > ol > li > div > div.info > div.hd > a > span:nth-child(1)')
            print(name.get_text())

if __name__== "__main__":
    cls = Douban()
    cls.get_top250()