# -*- coding:utf8 -*-


import glob
from chardet.universaldetector import UniversalDetector


detector = UniversalDetector()
for filename in glob.glob('*.csv'):
    print filename
    detector.reset()
    for line in file(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    print detector.result
    print ' '