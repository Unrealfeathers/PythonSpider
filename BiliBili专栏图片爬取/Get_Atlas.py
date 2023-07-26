import time
import os
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By


# todo 如果要使用协程，记得将延时函数缓换成协程专用的函数


class Atlas:
    url = ""
    save_path = "/Url"
    # 图集网页url储存字符组
    atlas_url_list_new = []
    atlas_url_list_old = []

    def __init__(self, up_url, file_path):
        self.url = up_url
        self.save_path = file_path + self.save_path
        if os.path.exists(self.save_path) is False:
            os.mkdir(self.save_path)

    def __read_old_url(self):
        # 读取已经爬取的url文件
        with open(self.save_path + "/AtlasUrl.txt", "r") as fp:
            for line in fp.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                self.atlas_url_list_old.append(line)

    def __write_new_url(self):
        # 储存图集网页url
        with open(self.save_path + "/AtlasUrl.txt", "a", encoding='utf-8') as fp:
            for new_url in self.atlas_url_list_new:
                fp.write(new_url)
                fp.write('\n')

    def get_url(self):
        if os.path.exists(self.save_path + "/AtlasUrl.txt"):
            self.__read_old_url()
        # 例化
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)
        driver.get(self.url)
        time.sleep(3)
        # 获取总页数
        page_num = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div/div/div[2]/ul/li[6]/a').text
        # 获取第一页图集网页url
        ul = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div/div/div[2]/div[2]/div/ul')
        li_list = ul.find_elements(By.TAG_NAME, 'li')
        # 储存图集url
        for li in li_list:
            atlas_url = li.find_element(By.TAG_NAME, 'a').get_property('href')
            if atlas_url not in self.atlas_url_list_old:
                self.atlas_url_list_new.insert(0, atlas_url)
            else:
                break
        print("第1页获取完毕\n")
        # 其它页
        flag = False
        for num in range(2, int(page_num) + 1):
            if flag:
                break
            driver.find_element(By.CLASS_NAME, 'be-pager-next').click()
            time.sleep(2)
            # 获取图集网页url
            ul = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div/div/div[2]/div[2]/div/ul')
            li_list = ul.find_elements(By.TAG_NAME, 'li')
            # 存放图集网页url
            for li in li_list:
                atlas_url = li.find_element(By.TAG_NAME, 'a').get_property('href')
                if atlas_url not in self.atlas_url_list_old:
                    self.atlas_url_list_new.insert(0, atlas_url)
                else:
                    flag = True
                    break
            print(f"第{num}页获取完毕\n")
        self.__write_new_url()


class Image:
    save_path = "/Image"      # 图集保存路径
    new_atlas_url_path = "/Url/AtlasUrl.txt"     # 图集路径
    old_atlas_url_path = "/Url/OldAtlasUrl.txt"     # 已爬取图集链接路径

    atlas_url_list = []     # 图集链接列表
    atlas_url_list_new = []     # 新的图集链接列表
    atlas_url_list_old = []     # 已爬取图集链接列表

    def __init__(self, file_path):
        self.save_path = file_path + self.save_path
        self.new_atlas_url_path = file_path + self.new_atlas_url_path       # Url文件路径
        self.old_atlas_url_path = file_path + self.old_atlas_url_path       # 已爬取的Url文件路径
        if os.path.exists(self.save_path) is False:
            os.mkdir(self.save_path)

    def __read_old_atlas_url(self):
        # 读取已经爬取的url文件
        with open(self.old_atlas_url_path, "r") as fp:
            for line in fp.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                self.atlas_url_list_old.append(line)

    def __read_new_atlas_url(self):
        # 读取新的url文件
        with open(self.new_atlas_url_path, "r") as fp:
            for line in fp.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                self.atlas_url_list_new.append(line)
# todo 对比找出新的url进行爬取
    def get_image(self):
        # url = 'https://movie.douban.com/j/chart/top_list'
        # param = {
        #     'type': '13',
        #     'interval_id': '100:90',
        #     'action': '',
        #     # 从数据库中第几个取数据
        #     'start': '0',
        #     # 一次取出的数据数量
        #     'limit': '20',
        # }
        # # UA伪装
        # header = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        # }
        # response = requests.get(url=url, params=param, headers=header)
        # list_data = response.json()
        # # 持久化储存
        # fp = open('./douban.json', 'w', encoding='utf-8')
        # json.dump(list_data, fp=fp, ensure_ascii=False)
        # print('OK')
        pass


if __name__ == '__main__':
    url = "https://www.bilibili.com/read/cv25060019"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183"
    }
    response = requests.get(url=url, headers=headers)
    with open("text.html", "a", encoding='utf-8') as f:
        f.write(response.text)
