from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import re
import csv


# 定义一个搜索商品的函数
def search_product(key_word):
    bro.maximize_window()
    # 定位搜索框并输入搜索关键词
    bro.find_element_by_id('q').send_keys(key_word)
    # 定位"搜索"按钮并点击
    bro.find_element_by_class_name('btn-search').click()
    # 等待30s，手动扫码登录吧
    time.sleep(30)
    page_total = bro.find_element_by_xpath('//div[@class="total"]').text
    page = re.findall('\d+', page_total)[0]
    return int(page)


# 定义一个获取数据的函数
def get_data():
    '''
    可以看到，每页的所有数据都在节点<div class="items">...<div>中，其每个子节点<div class ="item J_MouserOnverReq  "...<div>为一个商品的信息，每个商品都在目标数据中
    '''
    products = bro.find_elements_by_xpath('//div[@class="items"]/div[@class ="item J_MouserOnverReq  "]')
    # 此处注意find_elements_by_xpath()跟find_element_by_xpath()的区别
    for product in products:
        # 价格
        price = product.find_element_by_xpath('.//strong').text
        # 付款人数
        buy_num = product.find_element_by_xpath('.//div[@class ="deal-cnt"]').text
        # 商品描述
        description = product.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text
        # 店铺名
        shop = product.find_element_by_xpath('.//div[@class ="shop"]/a').text
        # 发货地
        place = product.find_element_by_xpath('.//div[@class ="location"]').text
        # 保存到本地csv文件
        with open('{}.csv'.format(key_word), mode='a', newline='', encoding='utf-8-sig') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([price, buy_num, description, shop, place])
    time.sleep(1)


# 定义一个翻页爬取数据的函数
def get_all_page_data(page):
    # 爬取第一页的数据
    get_data()
    print("第1页爬取成功")
    # 爬取余下页数的数据
    for i in range(page - 1):
        # 定位"下一页"按钮并点击
        bro.find_element_by_xpath('//li[@class="item next"]').click()
        # 给充足的时间等待页面完全加载
        print('页面加载中......')
        time.sleep(20)
        get_data()
        print('第', i + 2, '页爬取成功')


if __name__ == '__main__':
    key_word = input('请输入你想搜索的关键词：')
    # 规避检测
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 实例一个浏览器对象
    bro = webdriver.Chrome(options=option)
    bro.get('https://www.taobao.com/')
    page = search_product(key_word)
    get_all_page_data(page)
