#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import codecs


def main():
    inpath = 'output/Page.json'
    output = 'output/Page.qa'
    MAX_TITLE_LEN = 500
    USE_SUBTITLE = True
    with codecs.open(inpath, encoding='utf-8') as fi, \
        codecs.open(output, 'wb', encoding='utf-8') as fo:
        for line in fi:
            json_obj = json.loads(line.rstrip())
            url = json_obj['url']
            title = json_obj['title']
            subtitle = json_obj['subtitle']
            comments = json_obj['comments']
            if not comments:
                continue
            if USE_SUBTITLE:
                q = title + ' ' + subtitle
            else:
                q = title
            if len(q) > MAX_TITLE_LEN:
                continue
            q = q.lower()
            a = ' '.join(json_obj['comments']).lower()
            fo.write('%s\t%s\n' % (q, a))
    return None


if __name__ == '__main__':
    main()
