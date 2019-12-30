import re
import requests
import config
import time
start = time.time()
start_tuple=time.localtime()
start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_tuple)

# main_url = "https://ltv2060.cloudycdn.services/store/_definst_/tmsp00060/vodt/00/c3/240240/w98_D19-2100-0.smil/"
# url3="https://ltv2060.cloudycdn.services/store/_definst_/tmsp00060/vodt/00/c3/240240/w98_D19-2100-0.smil/chunklist_b1000000_sleng_t64U0Q=.m3u8?VThhlA715QEZbtrlQYE-8SFANLeoMRdsJ_AQYL4D5Fl_-6FSQnOYunbaYAl7ru3sskfu6MZeA1v91pnWd3YTDFQWmA529NOCl6I61zrVjH3D1YggZGF_4CvwIkxLOzDBvI_ftMxnfwNq1NE-JaqBxnHn4NNaI4D-AWgWcou-qjjT4y5rrFbSzlQLSF1ItPTDu8qB-HZcKlM"


main_url="https://ltv2060.cloudycdn.services/store/_definst_/tmsp00060/vodt/00/c3/240247/abi_N18-0580-0.smil/"
url3="https://ltv2060.cloudycdn.services/store/_definst_/tmsp00060/vodt/00/c3/240247/abi_N18-0580-0.smil/chunklist_b1000000_sleng_t64U0Q=_cfdG1zcDAwMDYwL3ZvZHQvMDAvYzMvMjQwMjQ3L04xOC0wNTgwLTAwMV9Nb2xpamFzX2xhdl8xX21wNC50dG1s.m3u8?gdqtUiOoyGmSQ4bSC-y3la9FXlxpYTXpt-TqAOUGSwVERBuGgprq-OVk0-AyXmg0bsxrAfSEAh1cisFieI91ne0W9iKxvs8XmqjioTIQE2u9bo5dmCpRLiK05NNqUXJcr1mBvp-NYOEXSYPtsV7l_o8hpaRQyeF3xV1nODvmGYp9rncHd0KqhfVIOPExUNAmJ2_94bqOCnkb"



r3 = requests.get(url3, proxies=config.proxies)
file_text=open(config.path+"links.txt",'w')
for link in r3.text.split('\n'):
    if re.findall('media_b1000000_sleng_t64U0Q=', link):
        # print(link)
        # print(main_url+link)
        file_text.write(str(main_url + link + '\n')) 
file_text.close()

link_ls=open(config.path+"links.txt",'r')
with open('movie.ts', 'wb') as f:
    for li in link_ls:
        r = requests.get(li.rstrip('\n'), proxies=config.proxies)
        f.write(r.content)

end = time.time()
end_tuple = time.localtime()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_tuple)
print("Script ended: "+end_time)
print("Script running time: "+time.strftime('%H:%M:%S', time.gmtime(end - start)))