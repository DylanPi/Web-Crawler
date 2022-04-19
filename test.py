'''
utf-8

李鹏海 3190105560

爬取网站视频
'''

import requests
from lxml import html
import asyncio
import os

def get_js_src(url):

    resp = requests.get(url)
    # print(resp.text)
    origin_html = html.etree.HTML(resp.text)
    res = origin_html.xpath('/html/script[2]/@src')
    return res[0]

def get_m3u8_src(url):
    dic = {}
    resp = requests.get(url)
    m3u8_lst=resp.text.split(';')[4:-2]
    for item in m3u8_lst:
        m3u8_url = item.split('=')[-1].strip('"').split(',')
        dic['playarr_'+str(m3u8_url[-1])]=m3u8_url[0]
    # print(dic)
    return dic

def download_m3u8_file(url_dic,position):
    for k,v in url_dic.items():
        resp = requests.get(v)
        with open(position+k+'.txt', 'wb') as f:
            f.write(resp.content)

def get_second_m3u8(url_dic,head):
    dic = {}
    for k in url_dic.keys():
        with open('./pachong/demo1/m3u8_1/'+k+'.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                else:
                    line = line.strip()
                    dic[k]=head + line
    download_m3u8_file(dic,'./pachong/demo1/m3u8_2/')

async def aio_download(dic,position):
    # position = ./pachong/demo1/
    video_position = position+'vedio/'
    #./pachong/demo1/vedio/
    session = requests.Session()
    for k in dic.keys():
        ks_vedio_position = video_position + k
        # ./pachong/demo1/vedio/playrry_1
        os.makedirs(ks_vedio_position, exist_ok=True)

        with open(f'{position}m3u8_2/{k}.txt','r',encoding='utf-8') as f:
            n=0
            for line in f:
                if line.startswith('#'): continue
                line = line.strip()
                n+=1
                download_ts(line,n,session,ks_vedio_position)
            with open(f'{ks_vedio_position}/sum.txt','w') as f:
                f.write(str(n))

def download_ts(url,filename,session,video_position):
    s = session.get(url)
    with open('{:}/{:0>3d}.ts'.format(video_position,filename),'wb') as f:
        f.write(s.content)
    print(f'{filename}over!')
    
def merge_ts(dic,position):
    # './pachong/demo1/'
    for k in dic.keys():
        vedio_position = f'{position}vedio/{k}'
        # './pachong/demo1/vedio/playarr_1'
        current_path = os.path.abspath(__file__).rsplit('\\',1)[0]
        vedio_path = f'{current_path}\\vedio\\{k}'
        #'c:\\Users\\Dylan\\Desktop\\python\\pachong\\demo1\\vedio\\{k}'
        os.system(f"copy /b {vedio_path}\\*.ts {vedio_path}\\{k}.mp4")

def main(url,head):
    # 1.找到页面源代码中的js文件地址
    js_url = get_js_src(url)
    # 2.拿到第一层m3u8的下载地址
    m3u8_dic=get_m3u8_src(js_url)
    # 3.下载第一层m3u8
    download_m3u8_file(m3u8_dic,'./pachong/demo1/m3u8_1/')
    # 4.下载第二层m3u8
    get_second_m3u8(m3u8_dic,head)
    # 5.下载视频
    asyncio.run(aio_download(m3u8_dic,'./pachong/demo1/'))
    # 6.需要解密先解密，如AES加密，在m3u8文件头部几行中可以知道
    # 7.合并ts文件
    merge_ts(m3u8_dic,'./pachong/demo1/')
    
if __name__ == '__main__':
    url='http://zikeke.net/acg/1605/1.html'
    # js_url="http://d.gqyy8.com:8077/ne2/s1605.js?1648712973"
    head='https://hey04.789zy.cc'
    main(url,head)