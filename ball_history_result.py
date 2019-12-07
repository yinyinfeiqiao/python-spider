import requests
# 使用BeautifulSoup,需要这么导入模块
from bs4 import BeautifulSoup


def historyResultJob(full_url):
    html = loda_data(full_url)
    parse_data = parse_page_data(html)
    write_page_data(parse_data);


def loda_data(url):
    req_header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response = requests.get(url, headers=req_header)
    if response.status_code == 200:
        return response.text


def write_page_data(data):
    """
    结果写入本地
    :param data:
    :return:
    """
    print(data)
    if len(data):
        filename = 'F:\\study\\bigdata\write_data.txt'
        with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            for tr in data:
                f.write('\t'.join(tr) + "\n")


def parse_page_data(html):
    """
    解析分页的页面源码数据
    :param html:
    :return:
    """
    """
    features=None：指明bs解析器
    lxml:使用lxml下的html解析器
    html.parser:是python自带的一个解析器模块
    """

    data = [];
    html_bs = BeautifulSoup(html, features='lxml')
    # html_bs.find():查找一个节点
    # html_bs.find_all():查找所有符合条件的节点
    """
    name=None, 指定你要查找的标签名,可以是一个字符串,正则表达式,或者列表
    attrs={}, 根据属性的值查找标签（dict）{'属性名称':'属性的值'}
    text=None, 可以是一个字符串,正则表达式,查找符合条件的文本内容
    limit=None　限制返回的标签的个数
    find_all方法返回的吧标签都放在列表中
    """
    tbody = html_bs.find(name='tbody')
    trs = tbody.find_all(name='tr')
    print(trs)
    for tr in trs:
        td = tr.select('td')
        data.append(
            [td[0].get_text(), td[1].get_text(), td[2].get_text(), td[3].get_text(), td[4].get_text(), td[5].get_text(),
             td[6].get_text(), td[7].get_text(), td[15].get_text()])
    return data


if __name__ == '__main__':
    full_url = 'https://datachart.500.com/ssq/history/newinc/history.php?start=1&end=19140'
    historyResultJob(full_url)
