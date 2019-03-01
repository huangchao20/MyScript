import os

def  SpliceSh(filename, mk):
    f1 = filename.split('\\')[-1]
    nfilename = filename.replace(f1, '222222222')
    with open(nfilename, 'w') as f:
        with open(filename, 'r') as fs:
            for fr in fs.readlines():
                if 'startflag' in fr:
                    f.write(mk)
                    f.write('\n')
                elif 'install' in fr and fr.endswith('.sh\n'):
                    f.write(fr)
                    f.write(mk)
                    f.write('\n')
                else:
                    f.write(fr)
    os.remove(filename)
    os.rename(nfilename, filename)

if __name__ == '__main__':
    filename = 'F:\\黄小宝的宝\测试目录\\fbap.20190110rw.t6\\sbin\\51.db2_insert_fbap_auto.sh'
    mk = 'install XQ-2018-747 TS_75705_FBAP_X_20190110.sh'
    SpliceSh(filename, mk)