import os

def Test1(filename, str1):
    bak = 'bak'
    with open(filename) as f:
        testl = []
        frlist = []
        for fr in f.readlines():
            if fr.startswith('bak'):
                testl.append(fr)
            frlist.append(fr)
        print(testl)
        print(frlist)
        nstr = 'bak%s' % (len(testl) + 1) + "=" + str1 + '\n'
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

if __name__ == '__main__':
    filename = 'F:\\黄小宝的宝\\script\\6.afa_workspace_pybak.sh'
    str1 = 'XQ-2018-801/TS_77044_AFA_20100117_pybak.sh'
    Test1(filename, str1)