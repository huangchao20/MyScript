import os
from shutil import copyfile
from public.PubFunc import PubDir
import re
class Mkdirs:
    """
    function:拼接conf, mkdirafa, mkdirafe文件
    """
    pot = "PORT"
    afa = 'inst1'
    afe = 'controller'
    sh = '.sh'

    def __init__(self, dpath, mkdirs):
        self.mkdirs = mkdirs                    #要被添加的内容
        self.dpath = dpath  #sbin上级目录
        self.sbin = 'sbin'
        self.mkafadir = '3.mkafadir.sh'         #添加afa目录
        self.mkafedir = '4.mkafedir.sh'         #添加afe目录
        self.fbap = '51.db2_insert_fbap_auto.sh'#fbapDB
        self.bsms = '52.db2_insert_bsms.sh'     #bsmsDB
        self.ami = '8.AMICInit.sh'          #刷内存
        self.pybak = '6.afa_workspace_pybak.sh'
        self.conf = 'cfgadd.sh'             #调用‘fbap_afa_afe_comm.conf.add’
        self.comm_conf = 'fbap_afa_afe_comm.conf.add'
        self.templateDir = PubDir().tmpDir()         #sbin模板路径
        self.mkNewFile()

    def tmp(self, dpath, sbinpath, filename):
        ret = os.path.join(sbinpath, filename)
        if filename not in os.listdir(sbinpath):
            tm = os.path.join(dpath, filename)
            if tm.endswith('.sh') and '51' in tm and self.ami not in os.listdir(sbinpath):
                # 拷贝刷内存的脚本到sbin目录
                ami = self.ami  # 刷内存的脚本
                fami = os.path.join(dpath, ami)
                ndir = os.path.join(sbinpath, ami)
                copyfile(fami, ndir)
            copyfile(tm, ret)
        return ret

    def checkFunc(self):
        """
        :function:根据入参mkdirs，调用不同的拼接函数
        :return:
        """
        print('开始调用Mkdirs')
        print('需要被拼接的内容：[%s]' % self.mkdirs)

    def mkNewFile(self):
        print("开始拼接:[%s]" % self.mkdirs)
        if os.path.isdir(self.dpath) and self.sbin not in os.listdir(self.dpath):
            os.chdir(self.dpath)
            os.mkdir(self.sbin)
        sbinpath = os.path.join(self.dpath, self.sbin)      #sbin目录
        lidir = os.listdir(sbinpath)
        if Mkdirs.pot in self.mkdirs:
            print('开始拼接配置文件：fbap_afa_afe_comm.conf.add')
            #将‘cfgadd.sh’文件移到sbin目录下面
            if self.conf not in lidir:
                conffilename = self.tmp(self.templateDir, sbinpath, self.conf)
                print(conffilename)
            #将‘fbap_afa_afe_comm.conf.add’文件移到sbin目录下面
            addfilename = self.tmp(self.templateDir, sbinpath, self.comm_conf)
            print(os.path.isfile(addfilename))
            with open(addfilename, "r+") as f:
                if self.mkdirs not in f.readlines():
                    f.write('\n')
                    f.write(self.mkdirs)
                    print('***拼接[%s]成功***' % addfilename)
            return "000000"
        elif Mkdirs.afa in self.mkdirs or Mkdirs.afe in self.mkdirs:
            if Mkdirs.afa in self.mkdirs:
                aa = self.mkafadir    #aa是afa或者afe的文件名
            else:
                aa = self.mkafedir
            print('开始拼接filename:[%s]' % aa)
            afafile = self.tmp(self.templateDir, sbinpath, aa)
            with open(afafile, 'r+') as f:
                f.readlines()
                f.write('\n')
                f.write(self.mkdirs)
            return '000000'
        elif Mkdirs.sh in self.mkdirs:
            print('开始处理执行脚本命令：【%s】' % self.mkdirs)
            if re.findall(r'\w{2}_\d{5}_\w_\d{8}.\w{2}', self.mkdirs):
                print('--------------------->>开始处理fbapDB命令:[%s]<<-----------------------' % self.mkdirs)
                filename = self.fbap
            elif re.findall(r'\w{2} \w{2}_\d{5}_\w{4}_\w{2}_\d{8}.sh', self.mkdirs):
                print('--------------------->>开始处理bsmsDB命令:[%s]<<-----------------------' % self.mkdirs)
                filename = self.bsms
            elif 'pybak' in self.mkdirs or "pyback" in self.mkdirs:
                print('-------------------->>开始处理【%s】<<----------------------' % self.mkdirs)
                filename = self.pybak
            shn = self.tmp(self.templateDir, sbinpath, filename)
            return '000000'
        else:
            print('请确认[%s] 是否有效' % self.mkdirs)
