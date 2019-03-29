# -*- coding: utf-8 -*
import os
import re
from nt import chdir

from bs4 import BeautifulSoup
from selenium import webdriver

site = 'https://www.missevan.com/sound/player?id=1016410'
dir_path = 'C:\\Users\ching\Desktop\\撒野第二季'


def get_all_ids(url):
    info_list = {}
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    browser = webdriver.Chrome(options=option)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    div = soup.find('div', attrs={'class': 'drama-episodes-nav'})
    # print(soup)
    for each_li in div.find_all('li'):
        title = each_li['title']
        a_href = each_li.find('a')['href']
        voice_id = re.split('\D', a_href)[-1]
        # print(title, voice_id)
        info_list[voice_id] = title
    return info_list


if __name__ == '__main__':
    # from page
    voice_info_list = get_all_ids(site)
    # or from file
    # voice_info_list = {}
    # with codecs.open('info.txt', 'r', 'utf-8') as fp:
    #     for line in fp:
    #         voice_info_list[re.split('\D', line)[0]] = re.split(' ', line)[1]
    for file_name in os.listdir(dir_path):
        try:
            value = voice_info_list[file_name]
            # print(file_name, value)
            if value:
                pre_name = os.path.join(dir_path, file_name)
                new_name = os.path.join(dir_path, value.rstrip() + '.mp3')
                chdir(os.path.dirname(pre_name))
                os.rename(pre_name, new_name)
                print(file_name + ' rename to ' + value.rstrip() + '.mp3')
        except KeyError as e:
            print("no such id : " + file_name)
