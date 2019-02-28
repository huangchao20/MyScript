import os

class ClassPyBak:
    def __init__(self, filename, mk):
        #mk = 'bak1=XQ-2018-758/TS_77575_AFA_20190221_pyback.sh'
        #sh ../$bak1
        self.filename = filename
        self.mk = mk

    def spliceMk(self):
        lpath, fdir, shname, filename = self.__spliceDir()
        print("【------开始组装sh脚本[%s]------】" % shname)
        print("任务编号[%s]" % fdir)
        print('脚本名:[%s]' % shname)

        ppath = os.path.join(lpath, fdir)
        print(ppath)

        flag = True
        startflag = "satrtflag"
        bak = "bak "

        os.chdir(ppath)
        nfilename = "22222222222.txt"
        os.rename(shname, nfilename)
        with open(nfilename, "r") as f:
            with open(shname, 'w+') as fn:
                for dd in f:
                    # 拼接：tmp = 'install XQ-2018-791 TR_45871_X_20181210.sh'
                    tmp = bak + fdir + " " + shname
                    if startflag in dd:
                        fn.write(tmp)
                    elif bak in dd and flag == True:
                        fn.write(dd)
                        fn.write(tmp)
                        flag = False
                    else:
                        fn.write(dd)
