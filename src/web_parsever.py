#_*_coding: utf-8 _*_
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import js2py
read_file = 'D:/homework/pythontest/test/input.txt'
write_file = 'D:/homework/pythontest/test/output.txt'

def web_parse(url):     # Function of Open HTML.
    try:
         print('start')
         html = urlopen(url).read().decode('utf-8')
    except HTTPError as e:
        print('fail : ',e.reason)
        html = None
    return html

def get_targeturl(url):      # Function of loading URL.
    host_url_https = re.findall('https://(.*?)/',url)
    host_url_http = re.findall('http://(.*?)/',url)
    if host_url_https:
        target_url = 'https://'+host_url_https[0]
    else:
        target_url = 'http://'+host_url_http[0]
    return target_url

def firstinnerparse(url):    # Fisrt Parsing + check inner html url to find REAL URl (in #document) 
    print('first & inner parse')
    link=''
    inner_html = []     #inner_html url list
    firsthtml = web_parse(url)   
    links = re.findall('<iframe (.*?)>', firsthtml) # Getting innerhtml link
    for linkElement in links:
        inner_html += re.findall('src="/PostView(.*?)"', linkElement)
    print(inner_html)   #inner_html is list of string
    if len(inner_html)>0:
        link = '/PostView' + inner_html[0]   #no need to parse hidden html(contain blog music)
        return link, False
    else:
        return url, True
    
def firstparse(url):    # Fisrt Parsing to find REAL URl (in #document) 
    print('firstparse')
    link=''
    inner_html = []     #inner_html url list
    firsthtml = web_parse(url)   
    links = re.findall('<iframe (.*?)>', firsthtml) # Getting innerhtml link
    for linkElement in links:
        inner_html += re.findall('src="(.*?)"', linkElement)
    print(inner_html)   #inner_html is list of string
    link = inner_html[0]   #no need to parse hidden html(contain blog music)
    return link

def secoundparse(url):  # Second Parsing of REAL URL
    print('secoundparse')
    pics, stickers, texts, text = [],[],[],[]  # arrays of pic, sticker, text.
    secondhtml = web_parse(url)  
    pics += re.findall('<img.*?src="(.*?)".*?data-width="(.*?)" data-height="(.*?)".*?>', secondhtml) #parse pics number
    print('1')
    stickers += re.findall('<img.*? src="(.*?)".*?class="se-sticker-image" />',secondhtml)  #parse sticker number
    print('2')
    texts += re.findall('<span.*?>(.*?)</span>',secondhtml) #parse text
    print('3')
    for parse in text:
        texts += re.findall("[가-힝 ]",parse)
    f = open(write_file,'a',-1,'utf-8')
    f.write('====================\n')
    for text in texts:
        f.write(text)
    f.write('\n')
    f.write('pics : ')
    f.write(str(len(pics)))
    f.write('\n')
    f.write('stickers : ')
    f.write(str(len(stickers)))
    f.write('\n====================\n')
    f.close()

def exceptionparse(url):
    print('exceptionparse')
    inner_html = []     #inner_html url list
    firsthtml = web_parse(url)   
    links = re.findall('<frame (.*?)>', firsthtml) # Getting innerhtml link
    for linkElement in links:
        inner_html += re.findall('src=\'(.*?)\'', linkElement)
    print(inner_html)  #inner_html is list of string 
    link = inner_html[0]  #no need to parse hidden html(contain blog music)
    return link

# Main function of "Parsing Phase"
def Parse(url):  # url = "https://blog.naver.com/~~~"
    target_url = get_targeturl(url)
    if re.match('https://blog.naver.com*.?',target_url):
        real_url, isinner_html=firstinnerparse(url)
        if isinner_html == False:
            print('False')
            link = target_url+real_url
        else:
            print('True')
            link = real_url
        print(link)
        secoundparse(link)
    elif re.match('https://m.blog.naver.com*.?',target_url):
        secoundparse(url)
    else:
        link = exceptionparse(url)
        target_url = get_targeturl(link)
        link = target_url + firstparse(link)
        print(link)
        secoundparse(link)


# Lines for Simple debugging.
if __name__ == "__main__":
    #url = 'http://asnote.net/221502461471'
    #url = 'http://o-goon.com/221287199411'
    #url = 'https://m.blog.naver.com/PostView.nhn?blogId=sw4r&logNo=221241276672&proxyReferer=https%3A%2F%2Fwww.google.com%2F'
    #url = 'https://blog.naver.com/invu1657/221473146800'
    #url = 'https://blog.naver.com/dragon1086/221037326999'
    #url = 'https://blog.naver.com/cwy5114/221492558752'
    #url = 'https://blog.naver.com/my_prayer_s2/221493594784'
    #url = 'https://blog.naver.com/kmh03214?Redirect=Log&logNo=221434499140'
    #Parse(url)
    f = open(read_file,'r')
    url_num = f.readline()
    for i in range(0,int(url_num)):
        url = f.readline()
        Parse(url)
        print('=====================\n')
    f.close()

"""     BeautifulSoup is too slow to use parsing program
    for links in link:
       print(links)
       html = web_parse(links)
    soup = BeautifulSoup(html,'html5lib')
    fixed_html = soup.prettify()
    print(fixed_html)   """
