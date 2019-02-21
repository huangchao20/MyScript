import os
from shutil import copyfile
from public.PubFunc import PubDir
class Mkdirs:
    """
    function:拼接conf, mkdirafa, mkdirafe文件
    """
    def __init__(self, dpath, mkdirs):
        self.mkdirs = mkdirs
        self.dpath = dpath  #sbin目录
        self.sbin = 'sbin'
        self.mkafadir = '3.mkafadir.sh'
        self.mkafedir = '4.mkafedir.sh'
        self.conf = 'cfgadd.sh'
        self.comm_conf = 'fbap_afa_afe_comm.conf.add'
        print(self.mkdirs)
        print(self.dpath)
        t = PubDir()
        self.templateDir = t.tmpDir()

    def mkNewFile(self):
        print("开始拼接:[%s]" % self.mkdirs)
        pot = "PORT"
        afa = 'inst1'
        afe = 'controller'

        if os.path.isdir(self.dpath) and self.sbin not in os.listdir(self.dpath):
            os.chdir(self.dpath)
            os.mkdir(self.sbin)

        sbinpath = os.path.join(self.dpath, self.sbin)

        #内置函数，拼接文件名的，返回拼接后的文件名
        def tmp(dpath, sbinpath, filename):
            ret = os.path.join(sbinpath, filename)
            if filename not in os.listdir(sbinpath):
                tm = os.path.join(dpath, filename)
                copyfile(tm, ret)
            return ret

        lidir = os.listdir(sbinpath)
        if pot in self.mkdirs:
            print('开始拼接配置文件：fbap_afa_afe_comm.conf.add')
            #将‘cfgadd.sh’文件移到sbin目录下面
            if self.conf not in lidir:
                conffilename = tmp(self.templateDir, sbinpath, self.conf)
                print(conffilename)

            #将‘fbap_afa_afe_comm.conf.add’文件移到sbin目录下面
            addfilename = tmp(self.templateDir, sbinpath, self.comm_conf)
            print('----------:[%s]----------:[%s]' % (self.mkdirs, addfilename))
            print(os.path.isfile(addfilename))

            with open(addfilename, "r+") as f:
                for i in f.readline():
                    print(i)
                f.write('\n')
                f.write(self.mkdirs)
                f.write('\n')
                print('***拼接[%s]成功***' % addfilename)
            return "000000"

        elif afa in self.mkdirs:
            print('开始拼接：3.mkafadir.sh')
            afafile = tmp(self.templateDir, sbinpath, self.mkafadir)
            with open(afafile, 'r+') as f:
                f.write(self.mkdirs)

        elif afe in self.mkdirs:
            print('开始拼接：4.mkafedir.sh')
            afefile = tmp(self.templateDir, sbinpath, self.mkafedir)
            with open(afefile, 'r+') as f:
                f.write(self.mkdirs)
        else:
            print('请确认[%s] 是否有效' % self.mkdirs)
