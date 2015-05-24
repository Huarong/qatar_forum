#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import re
import os
import logging
import codecs

def print_list(lst):
    for e in lst:
        print e

def init_log(logname, filename, level=logging.DEBUG, console=True):
    # make log file directory when not exist
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    logger = logging.getLogger(logname)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    fileHandler = logging.FileHandler(filename, mode='w')
    fileHandler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(fileHandler)
    if console:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

    return logger



def mkdir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return None


def main():
    logger = init_log('qatarliving', './log')
    categories = ['family-life-qatar', 'funnies', 'working-qatar',
    'salary-allowances', 'electronics-0', 'health-fitness', 'computers-internet',
    'opportunities', 'politics', 'beauty-style', 'qatari-culture', 'environment',
    'pets-animals', 'news', 'language', 'missing-home', 'company-news',
    'qatar-living-website', 'technology', 'ramadan', 'dining', 'fashion',
    'recipes', 'qatar-2022', 'movies-qatar']
    max_page = 2000
    base_url = 'http://www.qatarliving.com/forum/qatar-living-lounge?page=3'
    url_dir = './urls'
    mkdir(url_dir)
    for category in categories:
        continue_null_count = 0
        url_path = os.path.join(url_dir, category)
        f_url = codecs.open(url_path, 'wb', encoding='utf-8')
        s = requests.Session()
        for page in range(1, max_page):
            if page > max_page:
                logger.info('[touch max_page] category %s exit at page %s' % (category, page))
                break
            if continue_null_count > 5:
                logger.info('category %s exit at page %s' % (category, page - continue_null_count))
                break
            url = 'http://www.qatarliving.com/forum/%s?page=%s' % (category, page)
            try:
                r = s.get(url)
            except:
                continue
            url_pat = ur'<a href="(.+?/posts/.+?)"'
            url_reg = re.compile(url_pat)
            found = url_reg.findall(r.content)
            found = [e for e in found if '#comment' not in e]
            if len(found) > 14:
                found = found[:-14]
                continue_null_count = 0
                for e in found:
                    f_url.write('%s\n' % e)
                logger.info('finish %s' % url)
            else:
                logger.warning('invalid page: %s' % url)
                continue_null_count += 1
        f_url.close()


    # print_list(found)

if __name__ == '__main__':
    main()
