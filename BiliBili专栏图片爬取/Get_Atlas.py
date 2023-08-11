import time
import random
import os
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By

# todo 如果要使用协程，记得将延时函数缓换成协程专用的函数


class Atlas:
    # Url储存路径
    save_path = "/Url"
    # 图集网页url储存字符组
    atlas_url_list_new = []
    atlas_url_list_old = []

    def __init__(self, file_path):
        self.save_path = file_path + self.save_path
        if os.path.exists(self.save_path) is False:
            os.mkdir(self.save_path)

    def __read_old_url(self):
        # 读取已经爬取的url文件
        with open(self.save_path + "/AtlasUrl.txt", "r", encoding='utf-8') as fp:
            for line in fp.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                self.atlas_url_list_old.append(line)

    def __write_new_url(self):
        # 储存图集网页url
        with open(self.save_path + "/AtlasUrl.txt", "a", encoding='utf-8') as fp:
            for new_url in self.atlas_url_list_new:
                fp.write(new_url)
                fp.write('\n')

    def get_url(self, up_url):
        if os.path.exists(self.save_path + "/AtlasUrl.txt"):
            self.__read_old_url()
        # 例化
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)
        driver.get(up_url)
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

    random.seed("114514")

    images_save_path = "/Image"  # 图集保存路径
    atlas_url_path = "/Url/AtlasUrl.txt"  # 图集路径
    done_atlas_url_path = "/Url/FinishedAtlasUrl.txt"  # 已爬取图集链接路径

    atlas_url_list = []  # 图集链接列表
    atlas_url_list_done = []  # 已爬取图集链接列表
    atlas_url_list_tbd = []  # 新的图集链接列表
    img_urls = []  # 单图集内图片链接

    def __init__(self, file_path):
        self.images_save_path = file_path + self.images_save_path
        self.atlas_url_path = file_path + self.atlas_url_path  # Url文件路径
        self.done_atlas_url_path = file_path + self.done_atlas_url_path  # 已爬取的Url文件路径
        # 检查图片储存文件夹是否存在
        if os.path.exists(self.images_save_path) is False:
            os.mkdir(self.images_save_path)

    def __read_atlas_urls(self):  # 读取Atlas_Url.txt文件
        if os.path.exists(self.atlas_url_path) is False:
            print("请先爬取图集链接。")
        with open(self.atlas_url_path, "r", encoding='utf-8') as fp:
            for line in fp.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                self.atlas_url_list.append(line)

    def __read_done_atlas_urls(self):  # 读取已经爬取的url文件
        if os.path.exists(self.done_atlas_url_path) is True:
            with open(self.done_atlas_url_path, "r", encoding='utf-8') as fp:
                for line in fp.readlines():
                    line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                    self.atlas_url_list_done.append(line)
        else:
            pass

    def __get_new_atlas_url(self):  # 获取未爬取的URL
        self.__read_atlas_urls()
        self.__read_done_atlas_urls()
        for atlas_url in self.atlas_url_list:
            if atlas_url not in self.atlas_url_list_done:
                self.atlas_url_list_tbd.append(atlas_url)

    def __get_image_urls(self, url, headers):
        # 清空单个图集链接列表
        self.img_urls.clear()
        # 获取html文本
        response = requests.get(url=url, headers=headers).text
        # 实例化etree对象
        tree = etree.HTML(response, parser=etree.HTMLParser(encoding="utf-8"))
        # Xpath解析
        images = tree.xpath("/html/body/div[3]/div/div[3]/div[1]/div/div/figure")
        # 获取图集标题
        cv = url.split("/")[-1]
        title = tree.xpath("/html/body/div[3]/div/div[3]/div[1]/div[1]/h1/text()")
        # 获取图片Url和名称，并拼接
        num = 0  # 用于命名无名称图片
        for image in images:
            img_url = image.xpath("./img/@data-src")
            if not img_url:
                continue
            img_id = image.xpath("./figcaption/text()")
            if not img_id:
                img = "https:" + img_url[0] + "$" + str(num) + "." + img_url[0].split(".")[-1]
                num = num + 1
            else:
                img = "https:" + img_url[0] + "$id=" + img_id[0] + "." + img_url[0].split(".")[-1]
            self.img_urls.append(img)
        # 拼接文件名
        file_name = cv + "-" + title[0].split("\n")[-2]
        # 去除特殊符号，防止文件夹名不合法
        return file_name.replace(" ", "").replace(":", "：")

    def get_images(self, num, headers):
        # 获取未爬取的Url
        self.__get_new_atlas_url()
        # 逐个图集爬取
        for index, url in enumerate(self.atlas_url_list_tbd):
            # 获取单个图集内的图片Url和图集标题
            file_name = self.__get_image_urls(url=url, headers=headers)
            # 判断储存图集的文件夹是否存在
            if os.path.exists(self.images_save_path + "/" + file_name) is False:
                os.mkdir(self.images_save_path + "/" + file_name)
            # 逐张图片爬取
            for img_url in self.img_urls:
                # 生成图片名称
                img_name = img_url.split("$")[-1]
                if os.path.exists(self.images_save_path + "/" + file_name + "/" + img_name) is True:
                    continue
                try:
                    response = requests.get(url=img_url.split("$")[-2], headers=headers, timeout=10)
                    # response_time_a = response.elapsed.total_seconds()  # 获取请求响应时间
                    # print("响应时间" + str(response_time_a) + "秒")
                    img_data = response.content
                except Exception as e:
                    print("单张图片获取失败，正在重试!")
                    for i in range(100):  # 循环去请求网站
                        response = requests.get(url=img_url.split("$")[-2], headers=headers, timeout=10)
                        response_time_b = response.elapsed.total_seconds()  # 获取请求响应时间
                        print("循环第" + str(i) + "次")
                        if response_time_b < 10:  # 如果响应时间小于10秒，结束循环
                            img_data = response.content
                            break
                # 储存图片
                with open(self.images_save_path + "/" + file_name + "/" + img_name, 'wb') as fp:
                    fp.write(img_data)
            # 储存已经爬取的图集Url
            with open(self.done_atlas_url_path, "a", encoding='utf-8') as fp:
                fp.write(url)
                fp.write("\n")
            if index == num - 1:
                break


if __name__ == '__main__':
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183"
    }
    get_image = Image(".")
    get_image.get_images(num=10, headers=Headers)
    print("爬取完成！")
    pass
