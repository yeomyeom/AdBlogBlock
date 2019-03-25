#web parsing with beautifulsoup
#from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import re
def web_parse(url):
    try:
         print('start')
         html = urlopen(url).read().decode('utf-8')
    except HTTPError as e:
        print('fail : ',e.reason)
        html = None
    return html
def main():
    inner_html = []#inner_html url list
    pics = []#inner_html's pictures url
    num_pic = 0#pictures number
    target_url = 'https://blog.naver.com'
    url = 'https://blog.naver.com/nw_cool/221493950253'#later change current URL
    html = web_parse(url)
    link = re.findall('<iframe (.*?)>', html)
    for links in link:
        inner_html += re.findall('src="(.*?)"', links)
    print(inner_html) #inner_html is list of string
    for links in inner_html:
        links = target_url+links
        html = web_parse(links)
        pics += re.findall('<img src="https://blogfiles(.*?).jpg"', html)#count pics number
    print(pics)
    num_pic += len(pics)
    print(num_pic)
    #BeautifulSoup is too slow to use parsing program
    #for links in link:
    #    print(links)
    #    html = web_parse(links)
    #soup = BeautifulSoup(html,'html5lib')
    #fixed_html = soup.prettify()
    #print(fixed_html)
