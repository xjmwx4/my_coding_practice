#-*- coding: utf-8 -*-

# 功能：将指定目录下的文件编码方式统一改成 UTF-8-SIG 编码，并备份原文件

import codecs
import os
import shutil
import re
import chardet

# abspath = "E:\Programming\\tools" # 指定文件查找路径
abspath = os.getcwd() # os.getcwd() 获取当前工作路径

def convert_encoding_utf8(filename, target_encoding):
    # Backup the origin file.
    shutil.copyfile(filename, filename + '.bak')

    # convert file from the source encoding to target encoding
    content = codecs.open(filename, 'r').read()
    source_encoding = chardet.detect(content)['encoding']
    print "Old_coding:", source_encoding, filename
    print "Convert to UTF-8-SIG.", "Already Done."
    print ""
    content = content.decode(source_encoding, 'ignore') #.encode(source_encoding)
    codecs.open(filename, 'w', encoding=target_encoding).write(content)

def main():
    for root, dirs, files in os.walk(abspath):
        for f in files:
            if f.lower().endswith('.csv'):
                filename = os.path.join(root, f)
                try:
                    convert_encoding_utf8(filename, 'utf-8-SIG')
                except Exception, e:
                    print filename
                

def process_bak_files(action='restore'):
    for root, dirs, files in os.walk(abspath):
        for f in files:
            if f.lower().endswith('.csv.bak'):
                source = os.path.join(root, f)
                target = os.path.join(root, re.sub('\.csv\.bak$', '.csv', f, flags=re.IGNORECASE))
                try:
                    if action == 'restore':
                        shutil.move(source, target)
                    elif action == 'clear':
                        os.remove(source)
                except Exception, e:
                    print source
                

if __name__ == '__main__':
    # process_bak_files(action='clear')
    main()