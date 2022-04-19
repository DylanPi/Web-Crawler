# douban top250 movies

import csv
import re

import chardet
import requests

url='https://movie.douban.com/top250'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29'
}

resp = requests.get(url,headers=headers)
# encode_type = chardet.detect(resp.text)
# html = resp.text.decode(encode_type['encoding']) 
page_content = resp.text

obj = re.compile(r'''<li>.*?<div class="item">.*?<span class="title">(?P<Mname>.*?)</span>.*?<span class=".*?">&nbsp;/&nbsp;.*?</span>
                    .*?<br>(?P<Myear>.*?)&nbsp;/&nbsp;'''  ,re.S)

     
        #                             <span class="title">&nbsp;/&nbsp;The Shawshank Redemption</span>
        #                         <span class="other">&nbsp;/&nbsp;月黑高飞(港)  /  刺激1995(台)</span>
        #                 </a>


        #                     <span class="playable">[可播放]</span>
        #             </div>
        #             <div class="bd">
        #                 <p class="">
        #                     导演: 弗兰克·德拉邦特 Frank Darabont&nbsp;&nbsp;&nbsp;主演: 蒂姆·罗宾斯 Tim Robbins /...<br>
        #                     1994&nbsp;/&nbsp;美国&nbsp;/&nbsp;犯罪 剧情
        #                 </p>

                        
        #                 <div class="star">
        #                         <span class="rating5-t"></span>
        #                         <span class="rating_num" property="v:average">9.7</span>
        #                         <span property="v:best" content="10.0"></span>
        #                         <span>2589827人评价</span>
        #                 </div>

        #                     <p class="quote">
        #                         <span class="inq">希望让人自由。</span>
        #                     </p>
        #             </div>
        #         </div>
        #     </div>
        # </li>

res = obj.finditer(page_content)
with open('./pachong/demo1/data.csv','w') as f:
    csvWriter = csv.writer(f)
    for i in res:
        dic = i.groupdict()
        dic['Myear']=dic['Myear'].strip()
        csvWriter.writerow(dic.values())       
    # print(i.group('Mname'),end='\t\t\t')
    # print(i.group('Moname'),end='\t\t\t')
    # print(i.group('Myear'))
print('over!')
