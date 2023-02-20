import requests
from lxml import etree
import time
from requests.exceptions import RequestException
import matplotlib.pyplot as plt

# 先get一个url然后xpath进行解析出需要的names(x_ticks)然后二级href进行循环requests每次循环进行作品个数的计算(y_ticks)
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
try:
    headers = {
        'Cookie': 'll="118131"; bid=uX1WB72iQyk; ap_v=0,6.0; gr_user_id=d056fc5e-43a6-46ae-a60b-d591592d11a1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1674791209%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=30149280.1977501548.1670819651.1670819651.1674791209.2; __utmc=30149280; __utmz=30149280.1674791209.2.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=81379588.1536642566.1674791209.1674791209.1674791209.1; __utmc=81379588; __utmz=81379588.1674791209.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=DD9FF54DB649DE4BA973F37B4C1D995DD|b3496a002c40ec0c023b566604163705; __yadk_uid=ITgBXdHqBrlrUOucGcgfuIcti7YTimI1; __gads=ID=8da67153f5541936-22b5e2656ed90001:T=1674791231:RT=1674791231:S=ALNI_MbxnZeiLWXXjudy7gwlsIckL6BvuA; __gpi=UID=00000badc3eca4a9:T=1674791231:RT=1674791231:S=ALNI_MaLufTJxnWkuwAP-UnkCyIdo44tiA; __utmt_douban=1; __utmt=1; dbcl2="267020583:R4RPpXIsxHo"; ck=KJaj; push_noty_num=0; push_doumail_num=0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=68b40431-b19e-4837-8909-511b8abc78e9; gr_cs1_68b40431-b19e-4837-8909-511b8abc78e9=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_68b40431-b19e-4837-8909-511b8abc78e9=true; __utmb=30149280.13.10.1674791209; __utmb=81379588.13.10.1674791209; _pk_id.100001.3ac3=df351a9a963a329a.1674791209.1.1674794529.1674791209.',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55'
    }

    url = 'https://book.douban.com/'
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    doc = etree.HTML(response.text)
    names = doc.xpath('//li[1]/ul[@class="clearfix"]//li/a[@class="tag"]/text()')
    print("爬取图书种类列表: ")
    print(names)

    hrefs = doc.xpath('//li/ul[@class="clearfix"]//li/a/@href')
    print("二级链接: ")
    print(hrefs[:8])

    num_page_int = []
    y_ticks = []
    n = 0

    for i in hrefs[:8]:
        deep_url = 'https://book.douban.com' + i
        response_next = requests.get(url=deep_url, headers=headers)
        doc2 = etree.HTML(response_next.text)
        num_string = doc2.xpath('//div[@class="pub"]/text()')
        # print(num_string)

        num_page_str_list = doc2.xpath('//div[@class="paginator"]/a[last()]/text()')
        # num_page_str_list是网页上总共页数的str
        print(num_page_str_list)
        # 将str转为int进行运算
        p = int(num_page_str_list[0])
        # 输出int类型的p然后将其添加至num_page_int列表中方便之后进行总数运算
        print(p)
        num_page_int.append(p)
        print(num_page_int)
        # a是一页中作品总数，通过遍历进行计数
        a = 0
        for x in num_string:
            a = a + 1
        # 页数*每页作品数=result本类型作品总数，之后将result添加至y_ticks方便之后绘图
        result = a * num_page_int[n]
        y_ticks.append(result)
        print(y_ticks)
        n = n + 1
        print("程序sleep 3s,防止反爬")
        time.sleep(9)

    print("图像绘制中......")

    x = range(8)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(30, 20), dpi=100)
    axes[0].bar(x, y_ticks, width=0.5, label='数目柱状图')
    axes[1].pie(y_ticks, labels=('小说', '随笔', '日本文学', '散文', '诗歌', '童话', '名著', '港台'),
                autopct='%1.2f%%', )
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(names)
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[0].set_xlabel('图书种类')
    axes[0].set_ylabel('图书数目')
    axes[0].set_title('柱状图', fontsize=25)
    axes[1].set_xlabel('图书种类')
    axes[1].set_ylabel('图书数目')
    axes[1].set_title('饼图', fontsize=25)

    axes[0].legend(loc="best")
    axes[1].legend(loc="best")

    plt.show()
except RequestException:
    print(None)
