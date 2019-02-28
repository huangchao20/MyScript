import os
import re
from shutil import copyfile
from app.Mkdirs import Mkdirs

class CheckSql:
    def __init__(self, dpath, sbindir, shstr):
        """
        :dpath:被校验的sh脚本名称
        :shname:sbin目录
        :shstr:脚本添加内容
        :param dpath:
        :param shname:
        :param mkdirs:
        """
        self.pybaksh = '6.afa_workspace_pybak.sh'
        self.fbap = '51.db2_insert_fbap_auto.sh'#fbapDB
        self.bsms = '52.db2_insert_bsms.sh'     #bsmsDB

        self.pybak = 'pybak'
        self.dpath = dpath
        self.delete = "delete"
        self.Del = 'del'
        self.sbindir = sbindir
        self.shstr = shstr
        self.TransFunc()

    def TransFunc(self):
        """
        描述：根据self.dpath的不太，调用不同的处理函数
        :return:
        """
        if self.pybak in self.dpath:
            self.__PyBak()
        else:
            ret = self.FindSh()
            if ret == '000000':
                print('OK~~')
                ret = self.__FindSbin()

    def __spliceDir(self):
        shdirs = self.dpath.split("\\")
        shname = shdirs.pop()   #sh脚本名
        fdir = shdirs.pop()     #任务编号

        lpath = '\\'.join((shdirs[0], ""))
        for i in range(1, len(shdirs)):
            lpath = os.path.join(lpath, shdirs[i])
        sbindir = os.path.join(lpath, 'sbin')
        print('lpath----->>[%s];sbindir---->>[%s]' % (lpath, shdirs))
        if re.findall(r'\w{2}_\d{5}_\w_\d{8}.\w{2}', shname):
            filename = os.path.join(sbindir, '8.AMICInit.sh')
            print('filename:[%s]' % filename)
        return lpath, fdir, shname, filename

    def __SpliceSh(self):
        """
        filename, lpath, fdir, shname
        name:__SpliceSh
        function:查看拼接指令是否在sh脚本中存在，如果不存在，则拼接操作指令
        F:\\黄小宝的宝\\测试目录\\fbap.20190110rw.t6\sbin\\6.afa_workspace_pybak.sh
        mkdirs = XQ-2018-801/sh TS_77044_AFA_20100117_pybak.sh---->>pybak"""

        lpath, fdir, shname, filename = self.__spliceDir()
        print('--------------->>开始执行__SpliceSh函数<<---------------')
        print("【------开始组装sh脚本[%s]------】" % shname)
        print("任务编号[%s]" % fdir)
        print('脚本名:[%s]' % shname)

        ppath = os.path.join(lpath, fdir)
        print(ppath)
        flag = True
        startflag = "satrtflag"
        install = "install "
        os.chdir(ppath)
        nfilename = "22222222222.txt"
        os.rename(shname, nfilename)
        with open(nfilename, "r") as f:
            with open(shname, 'w+') as fn:
                for dd in f:
                    # 拼接：tmp = 'install XQ-2018-791 TR_45871_X_20181210.sh'
                    tmp = install + fdir + " " + shname
                    if startflag in dd:
                        fn.write(tmp)
                    elif install in dd and flag == True:
                        fn.write(dd)
                        fn.write(tmp)
                        flag = False
                    else:
                        fn.write(dd)
        os.remove(nfilename)            #删除nfielname,防止处理下个文件报错

    def __PyBak(self):
        """
        描述：拼接代码备份脚本
        :return:
        """
        print('处理代码备份脚本[%s]------->>[%s]' % (self.sbindir, self.shstr))
        print('尼玛， 老子还没有开始呢')
        bak = 'bak'
        filename = os.path.join(self.sbindir, self.pybaksh)
        print('-------------------->filename:[%s]' % filename)
        if os.path.isfile(filename):
            with open(filename) as f:
                testl = []
                frlist = []
                for fr in f.readlines():
                    if fr.startswith('bak'):
                        testl.append(fr)
                    frlist.append(fr)
                print(testl)
                print(frlist)
                nstr = 'bak%s' % (len(testl) + 1) + "=" + self.shstr + '\n'
                carr = 'sh' + ' ' + '../$bak%s' % (len(testl) + 1)
                for i in range(len(frlist)):
                    if testl[-1] == frlist[i]:
                        frlist.insert((i + 1), nstr)
                print(frlist)
                # sh ../$bak1
                with open(filename, 'w') as f:
                    for fl in frlist:
                        f.write(fl)
                    f.write('\n')
                    f.write(carr)
        else:
            raise EOFError("请确认filename:[%s]是否存在" % filename)

    def __FindSbin(self):

        """
        name:__FindSbin
        function:查找sbin目录是否存在，如果不存在，则创建目录，并添加sh脚本
        """
        lpath, fdir, shname, filename = self.__spliceDir()
        print('lpath-------->%s' % lpath)
        print('fdir------->%s' % fdir)
        print('shname------>%s' % shname)
        print('filename------>%s' % filename)
        templateDir = "F:\\黄小宝的宝\\script\\sbin"         #sbin模板的路径
        print("***********开始查找[%s]下是否存在sbin目录***********" % lpath)
        sbin = "sbin"
        if sbin not in os.listdir(lpath):
            os.chdir(lpath)
            os.mkdir(sbin)
            os.chdir(fdir)
        sbindir = os.path.join(lpath, sbin)
        if re.findall(r"TS_\d{5}_\w_\d{8}.sh", shname):
            #检查8.AMICInit.sh脚本是否存在,如果不存在，则将文件拷贝过来
            if "8.AMICInit.sh" not in os.listdir(sbindir):
                copyfile(os.path.join(templateDir, "8.AMICInit.sh"), os.path.join(sbindir, "8.AMICInit.sh"))

            """判断shname安装手册是否提示部署"""
            """此处调用函数判断"""
            # with open(shname, 'r') as f:
            #     for dd in f:
            #         if ".sql" in dd:
            #             #从"db2 -tvf ./TS_75760_FBAP_D_20190117_01.sql|tee -a $LOGSNAME"切割出.sql文件名
            #             sqlfile = dd.split("./")[1].split("|")[0]
            #             print(sqlfile)
            #             """判断sqlfile是否存在"""
            #             if sqlfile not in os.listdir(os.getcwd()):
            #                 raise EOFError("[%s]调用的[%s]不存在，请确认" % (shname, sqlfile))
            #             else:   #检查部署的sql文件中是否包含delete语句
            #                 with open(sqlfile) as fsql:
            #                     for tmp in fsql:
            #                         if self.Del in tmp or self.Del.upper() in tmp:
            #                             raise EOFError("部署的[%s]文件中包含delete语句，请开发人员确认" % sqlfile)
            sbinShName = "51.db2_insert_fbap_auto.sh"
        elif "pybak" in shname:
            sbinShName = "6.afa_workspace_pybak.sh"

        t = os.path.join(templateDir, sbinShName)
        filename = os.path.join(os.path.join(lpath, sbin), sbinShName)
        if os.path.isfile(t) and sbinShName not in os.listdir(os.path.join(lpath, sbin)):
            copyfile(t, filename)
            #查找需要被拼接的脚本
            # 开始拼接sh脚本
        print('>>>>>>>>>>>>>>>>开始调用__SpliceSh函数<<<<<<<<<<<<<<<<<<<')
        self.__SpliceSh()

    def FindSh(self):
        print("**************开始检查sh脚本【%s】**************" % self.dpath)
        print("dpath: ", self.dpath)
        pybak = "pybak"
        sql = '.sql'
        shna = self.dpath.split('\\').pop()
        print('fbapDB脚本的文件名:[%s]' % shna)

        if not os.path.isfile(self.dpath):
            print('【%s】不存在，请开发确认' % self.dpath)
            raise EOFError("[%s]文件不存在，请确认" % self.dpath)
        #检查fbapdb脚本中是否存在del的sql文件
        with open(self.dpath, 'r+') as f:
            for fr in f:
                if self.Del in fr and sql in fr:
                    raise EOFError('[%s]文件中存在del文件，请注意检查' % self.dpath)
                elif self.Del not in fr and sql in fr:
                    for sqlname in fr.split(" "):
                        if sql in sqlname:
                            #原始的sqlname='./TS_0818000015_75994_third.cfg.sql|tee'
                            #新拼接的sqlname='TS_0818000015_75994_third.cfg.sql'
                            sqlname = sqlname.split('/')[1].split('|')[0]
                        if sqlname.endswith(sql):
                            sqlname = self.dpath.replace(shna, sqlname)
                            print('[%s]脚本中的文件[%s]' % (shna, sqlname))
                            if not os.path.isfile(sqlname):
                                raise EOFError('[%s]文件不存在，请检查' % sqlname)
                            with open(sqlname, 'r+') as f:
                                for sqlfr in f:
                                    if (self.delete in sqlfr or self.delete.upper() in sqlfr)\
                                              and not sqlfr.startswith('--'):
                                        raise EOFError("【%s】sql文件中存在delete语句:[%s]" % (sqlname, sqlfr))

        return "000000"

    def checkSh(filename):
        pass