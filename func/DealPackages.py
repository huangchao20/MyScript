#encoding=utf-8
import os
import docx
from win32com import client as wc
import re

from app.checkSqlBySh import CheckSql
from app.Mkdirs import Mkdirs

class DealPack:
    def __init__(self, dpath):
        self.dpath = dpath

    def __dealDocxFile(self, filename):
        """
         :function:word文档处理
         :param filename:
         :return:
         """
        print("【*****__dealDocxFile开始处理文档[%s]*****】" % filename)
        if os.path.isfile(filename):
            sfile = ('XQ', 'BUG', 'TR')
            listdir = filename.split('\\')
            listdir.pop()
            if listdir[-1].startswith(sfile):
                listdir.pop()
            # 组建路径‘F:\\TFS_l\\文档&DB&AFEjar包\\WEEK\\2019\\20190117’
            mkpth = '\\'.join((listdir[0], ""))
            for p in listdir[1:]:
                print(p)
                mkpth = os.path.join(mkpth, p)
            print('sbin的目录是[%s]' % mkpth)
            print(filename)
            file = docx.Document(filename)
            # 处理docx文档中的表格，处理cfg文件
            tables = file.tables

            for table in tables:
                for i in range(1, len(table.rows)):
                    result = table.cell(1, 0).text
                    if "PORT" in result:
                        print(result)
                mk = Mkdirs(mkpth, result)
                mk.mkNewFile()

            print("段落数: ", str(len(file.paragraphs)))
            # 输出段落编号及段落内容
            for i in range(len(file.paragraphs)):
                # print("第" + str(i) + "段的内容是：" + file.paragraphs[i].text)
                """
                re.findall(r'\w{2} \w{2}_\d{5}_X_\d{8}.\w{2}', file.paragraphs[i].text)     #匹配fbapDB
                re.findall(r'\w{2} \w{2}_\d{5}_\w{3}_\d{8}_pybak.sh', file.paragraphs[i].text)      #匹配pybak.sh
                re.findall(r'\w{2} \w{2}_\d{5}_\w{4}_\w{2}_\d{8}.sh', file.paragraphs[i].text)        #匹配bsmsDB
                """
                # 检查安装手册里面的文档是否存在
                if file.paragraphs[i].text.endswith('.sh'):
                    t =  file.paragraphs[i].text.split(' ')
                    for n in range(len(t)):
                        if t[n].endswith('.sh'):
                            rename = t[n]
                    f = filename.split('\\').pop()
                    # nfilename = filename.replace(f, file.paragraphs[i].text)
                    nfilename = filename.replace(f, rename)
                    print('新拼接的文件名是[%s]' % nfilename)
                    if not os.path.isfile(nfilename):
                        print("安装手册[%s]中的文件[%s]不存在" % (filename, nfilename))
                        return None
                    else:  # 拼接sbin下面所有的sh、add文件
                        if re.findall(r'\w{2} \w{2}_\d{5}_X_\d{8}.\w{2}', file.paragraphs[i].text):
                            print('【************bsmsDB开始处理：[%s]************】' %file.paragraphs[i].text)
                            print('fbapdb:[%s]' % file.paragraphs[i].text)
                        elif re.findall(r'\w{2} \w{2}_\d{5}_\w{4}_\w{2}_\d{8}.sh', file.paragraphs[i].text):
                            print('【************fbapDB开始处理：[%s]************】' % file.paragraphs[i].text)
                            print('bsmsdb:[%s]' % file.paragraphs[i].text)
                            tli = file.paragraphs[i].text.split(" ")
                            for name in tli:
                                if name.endswith('.sh'):
                                    shname = filename.replace(f, name)
                                    print('【***************shname[%s]**************】' % shname)
                                    cs = CheckSql(shname)

                        elif re.findall(r'\w{2} \w{2}_\d{5}_\w{3}_\d{8}_pybak.sh', file.paragraphs[i].text):
                            print('【************pybak开始处理：[%s]************】' % file.paragraphs[i].text)
                            print('pybak:[%s]' % file.paragraphs[i].text)
                        elif "mkdir" in file.paragraphs[i].text:  # 拼接afa、afe的sh脚本
                            mkdirs = file.paragraphs[i].text
                            if "inst1" in mkdirs:
                                print('afa:[%s]' % mkdirs)
                            else:
                                print('afe:[%s]' % mkdirs)
                            mk = Mkdirs(mkpth, mkdirs)
                            mk.mkNewFile()

    def TextFile(self):
        dlist = self.dpath.split('\\')
        print(dlist)
        filename = self.dpath
        if os.path.isfile(self.dpath):
            print("DealPack-->>self.dpath[%s]" % filename)
            dfile = os.path.splitext(filename)
            if dfile[1] == ".docx":  # 处理docx文件
                self.__dealDocxFile(filename)
            elif dfile[1] == ".doc":  # 将doc文件转换成docx文件
                print("处理doc文件[%s]..." % filename)
                w = wc.Dispatch('Word.Application')
                doc = w.Documents.Open(filename)
                newfile = "".join((dfile[0], ".docx"))
                doc.SaveAs(newfile)
                self.__dealDocxFile(newfile)
        return '000000'