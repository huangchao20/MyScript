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


def test(filename, mk):
    flag = True
    f1 = filename.split('\\')[-1]
    nfilename = filename.replace(f1, '222222222')
    try:
        with open(nfilename, 'w') as f:
            with open(filename, 'r') as fs:
                for fr in fs.readlines():
                    if 'startflag' in fr:
                        f.write(mk)
                        f.write('\n')
                    elif 'install' in fr and fr.endswith('.sh\n') and flag == True:
                        f.write(fr)
                        f.write(mk)
                        flag = False
                        f.write('\n')
                    else:
                        f.write(fr)
        os.remove(filename)
        os.rename(nfilename, filename)
    except Exception as e:
        print(e, filename)

if __name__ == '__main__':
    filename = 'F:\\黄小宝的宝\\script\\51.db2_insert_fbap_auto.sh'
    mks = ['install XQ-2018-753 TS_75705_FBAP_X_20190110.sh',\
           'install XQ-2018-748 TS_75705_FBAP_X_20190110.sh',\
           'install XQ-2018-749 TS_75705_FBAP_X_20190110.sh',\
           'install XQ-2018-750 TS_75705_FBAP_X_20190110.sh',\
           'install XQ-2018-751 TS_75705_FBAP_X_20190110.sh',\
           'install XQ-2018-752 TS_75705_FBAP_X_20190110.sh']
    for mk in mks:
        test(filename, mk)