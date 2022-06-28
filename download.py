import re
import os
import config
import requests
from requests.api import get
import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
def download_file(url, file_name):
        with open(file_name, "wb") as file:
                response = get(url)
                file.write(response.content)

try:
        link = input("Enter the link to download: ")
        options = Options()
        # options.add_argument("--headless")
        # driver = webdriver.Chrome(config.path_to_chromedriver, options=options)
        driver = webdriver.Firefox(executable_path=config.path_to_geckodriver)
        driver.get(link)
        print("Please wait couple seconds...")
        time.sleep(3)
        for elem in driver.find_elements(By.XPATH, "//iframe"):
                if elem.get_attribute("title") == "LTV Embed":
                        driver.switch_to.frame(elem)
                        for elem in driver.find_elements(By.XPATH, "//*"):
                                if elem.get_attribute("title") == 'Atskaņot video':
                                        elem.click()
                                        time.sleep(3)
                                        for request in driver.requests:
                                                if str(request.url).startswith('https://ltv2060.cloudycdn.services'):
                                                        if 'playlist' in request.url:
                                                                if 'm3u8' in request.url:
                                                                        download_file(request.url, 'playlist.m3u8')
                                                                        playlist_url=str(request.url)
                                        driver.close()
                                        url_end = re.search(r'(?<=playlist.m3u8).*', playlist_url).group(0)
                                        url_start = playlist_url.split('playlist')[0]
                                        open_file = open('playlist.m3u8', 'r')
                                        lines = open_file.readlines()
                                        resolution_dic={}
                                        for line in lines:
                                                if 'RESOLUTION=' in line:
                                                        resolution = (line.split('RESOLUTION=')[1]).replace('\n', '')
                                                        if ',' in resolution:
                                                                resolution=resolution.split(',')[0]
                                                                url_link = (lines[lines.index(line)+1]).replace('\n', '')
                                                                resolution_dic[resolution] = url_link
                                                        else:
                                                                url_link = (lines[lines.index(line)+1]).replace('\n', '')
                                                                resolution_dic[resolution] = url_link
                                        keys=[]
                                        for key, value in resolution_dic.items():
                                                keys.append(key)     
                                        input_resolution = input(f'Choose resolution:\n1: {keys[0]}\n2: {keys[1]}\n3: {keys[2]}\n')
                                        if input_resolution == '1':
                                                url_resolution = resolution_dic[keys[0]]
                                                download_file(url_start+url_resolution+url_end, f'chunklist_{keys[0]}.m3u8')
                                        if input_resolution == '2':
                                                url_resolution = resolution_dic[keys[1]]
                                                download_file(url_start+url_resolution+url_end, f'chunklist_{keys[1]}.m3u8')
                                        if input_resolution == '3':
                                                url_resolution = resolution_dic[keys[2]]
                                                download_file(url_start+url_resolution+url_end, f'chunklist_{keys[2]}.m3u8')
                                        file_name = input('Enter file name: ')
                                        print('Downloading...')
                                        for file in os.listdir('.'):
                                                if 'chunklist' in file:
                                                        file_to_open = file
                                                        break
                                        open_file=open(file_to_open, 'r')
                                        lines = open_file.readlines()
                                        download_url_list = []
                                        for line in lines:
                                                with open(file_name+'.ts', 'wb') as f:
                                                        if '.ts' in line and '#EXT-X-ENDLIST' not in line:
                                                                download_url=str(url_start+line.replace('\n', '')+url_end)
                                                                download_url_list.append(download_url)
                                        with open(file_name+'.ts', 'wb') as f:
                                                for li in download_url_list:
                                                        r = requests.get(li.rstrip('\n'))
                                                        f.write(r.content)
                                        os.remove(file_to_open)
                                        os.remove('playlist.m3u8')
                                        print('Done!')
                                        break
except Exception as e:
        pass
