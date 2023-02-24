from urllib import request
from bs4 import BeautifulSoup
import ssl
import collections
import random
import re
import os
import time
import sys
import types
import threading

MAX_THREADS = 30
semaphore = threading.Semaphore(MAX_THREADS)
event = threading.Event()


class download(object):
    def __init__(self, target):
        self.__target_url = target
        self.__head = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
        }
        self.__proxy = {
            'http': 'http://{}'.format('127.0.0.1:7892'),
            'https': 'https://{}'.format('127.0.0.1:7893'),
        }
        self.url = "https://www.soquwu.com"
        self.final_text = {}
        self.finished_num = 0
        self.total_num = 0

    def get_download_url(self, url):
        charter = re.compile(u'[第弟](.+)章', re.IGNORECASE)
        target_req = request.Request(url=url, headers=self.__head)
        target_response = request.urlopen(target_req)
        target_html = target_response.read().decode('gbk', 'ignore')
        listmain_soup = BeautifulSoup(target_html, 'lxml')
        title = listmain_soup.find_all('div', id='info')
        if len(title) == 0:
            self.GetRealUrl(-1, listmain_soup)
        else:
            title_soup = BeautifulSoup(str(title), 'lxml')
            novel_name = str(title_soup.h1).split(">")[1][:-4]
            flag_name = "《" + novel_name + "》" + "正文"

            chapters = listmain_soup.find_all('div', id='list')
            download_soup = BeautifulSoup(str(chapters), 'lxml')
            numbers = (len(download_soup.dl.contents) - 1) / 2 - 8
            download_dict = collections.OrderedDict()
            begin_flag = False
            numbers = 1
            for child in download_soup.dl.children:
                if child != '\n':
                    if child.string == u"%s" % flag_name:
                        begin_flag = True
                    if begin_flag == True and child.a != None:
                        download_url = self.url + child.a.get('href')
                        download_name = child.string
                        name = str(download_name)
                        #print(numbers)
                        #import pdb;pdb.set_trace()
                        download_dict[name] = download_url
                        numbers += 1
            self.total_num = numbers
            return novel_name + '.txt', download_dict

    def Downloader(self, charpter_num, chapter_name, url):
        with semaphore:
            text = self.get_text(charpter_num, url)
            self.final_text[chapter_name] = {
                "index": charpter_num,
                "content": text
            }
        event.set()

    def get_text(self, charter_num, url, index=0):
        download_req = request.Request(url=url, headers=self.__head)
        download_response = request.urlopen(download_req)
        download_html = download_response.read().decode('gbk', 'ignore')
        soup_texts = BeautifulSoup(download_html, 'lxml')
        texts = soup_texts.find_all(id='content')

        try:
            soup_text = BeautifulSoup(str(texts),
                                      'lxml').div.text.replace('app2();', '')
        except:
            if (index == 0):
                print(f"章节{charter_num}错误 重试第" + str(index + 1) + "次")
                return self.GetRealUrl(charter_num, str(soup_texts), index)
            else:
                print("章节再次错误")
                soup_text = ""
        soup_text = re.sub(u'[\'(https].*[.com]', '', soup_text)
        soup_text = re.sub(u'([\s][\s])', '\n\n', soup_text)
        self.finished_num += 1
        sys.stdout.write("已下载:%.3f%%" %
                         float(self.finished_num * 100 / self.total_num) +
                         '\r')
        sys.stdout.flush()
        return soup_text

    def Writer(self, name):
        path = f"./novels/{name}"
        if name in os.listdir("./novels/"):
            os.remove(path)
        content_dic = sorted(self.final_text.items(),
                             key=lambda k: (k[1]["index"]))
        with open(path, 'a', encoding='utf-8') as f:
            for chapter_name, text in content_dic:
                write_flag = True
                f.write(chapter_name + '\n\n')
                for each in text["content"]:
                    if each == 'h':
                        write_flag = False
                    if write_flag == True and each != ' ':
                        f.write(each)
                    if write_flag == True and each == '\r':
                        f.write('\n')
                f.write('\n\n')

    def GetRealUrl(self, charter_num, soup_texts, index=0):
        p = re.compile(u'\'[\w!@#$%^&/.=?]*\'"')
        p2 = re.compile(u'\'[0-9\w!@#$%&/.=?]+\'')
        s = str(soup_texts)
        strings = re.findall(p2, s)
        url = ""
        for ss in strings:
            url = ss.strip('\'') + url
        url = self.url + url
        print(url)
        if charter_num != -1:
            return self.get_text(charter_num, url, index + 1)
        else:
            return self.get_download_url(url)


if __name__ == "__main__":
    print(
        "\n\t\t欢迎使用《搜趣屋》小说下载小工具\n\n\t\t搜趣屋网址: https://www.soquwu.com\n\n\t\t作者:potato\t时间:2020-2-13\n"
    )
    print(
        "*************************************************************************"
    )
    target_url = str(input("请输入小说目录下载地址:\n"))
    # target_url = "https://www.soquwu.com/90_90897/"
    d = download(target=target_url)
    name, url_dict = d.get_download_url(target_url)

    index = 1

    print("《%s》下载中:" % name[:-4])
    threads = []
    index = 1
    lock = threading.Lock()
    for chapter_name, chapter_url in url_dict.items():
        thread = threading.Thread(target=d.Downloader,
                                  args=(index, chapter_name, chapter_url))
        threads.append(thread)
        thread.start()
        index += 1

    # total_size = len(url_dict)
    # with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
    #     progress = d.finished_index
    #     while progress < total_size:
    #         progress = d.finished_index
    #         pbar.update(progress - pbar.n)

    for thread in threads:
        thread.join()

    d.Writer(name)
    print("《%s》下载完成！" % name[:-4])