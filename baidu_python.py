#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from HTMLParser import HTMLParser
import os

def _attr(attrlists,attrname):
    for attr in attrlists:
        if attr[0] == attrname:
            return attr[1]
    return None

class PythonerParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_a = False
        self.all_pythoner = {}


    def handle_starttag(self, tag, attrs):
        if tag == 'a' and _attr(attrs, 'class') == 'avatar':
            self.in_a = True
        if tag == 'img' and self.in_a:
            self.all_pythoner['img_src'] = _attr(attrs, 'src')
            # print(self.all_pythoner)
        if tag == 'a' and _attr(attrs, 'class') == 'user_name':
            self.all_pythoner['pname'] = _attr(attrs, 'title')
            print(self.all_pythoner)
            pythoner_img_download(self.all_pythoner)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_a = False

def pythoner_img_download(all_pythoner):
    save_path = 'pythoner_imgs'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    r = requests.get(all_pythoner['img_src'])
    with open(save_path + '/' + all_pythoner['pname']+'.jpg', 'wb') as f:
        f.write(r.content)

def pythoner_download():
    for i in range(10):
        url = 'http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=python&pn=%d' % (i+1)
        r = requests.get(url)
        parser = PythonerParser()
        parser.feed(r.content)

if __name__ == '__main__':
    a = pythoner_download()
