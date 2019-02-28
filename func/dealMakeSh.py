import os
import re


class Make:
    def __init__(self, filename, mk):
        self.mk = mk
        self.filename = filename

    def spliceSh(self):
        print('【>>>>>>>>>Make Begin<<<<<<<<<<<】')
        print('【>>>>>>>>>开始处理[%s]<<<<<<<<<】' % self.filename)
        with open(self.filename, 'r+') as f:
            f.readlines()
            f.write(self.mk)
