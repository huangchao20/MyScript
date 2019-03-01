from watchdog.observers import Observer
from watchdog.events import *
import time

from DealPackages import DealPack

"""
监测文件夹、文件是否有变化
"""
class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def __filecheck(self, dpath):
        dp = DealPack(dpath)
        # print(dp.TextFile())
        ret = dp.TextFile()
        return ret

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))


    def on_created(self, event):
        docx_name = "安装"
        docx_list= ('docx', 'doc')
        dpath = event.src_path
        if event.is_directory:
            # print("directory created:{0}".format(event.src_path))
            print("OK")
        else:
            if event.src_path.endswith(docx_list) and docx_name in event.src_path:
                print("file created:{0}".format(event.src_path))
                t = self.__filecheck(dpath)

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))

if __name__ == "__main__":
    dpath = "F:\\黄小宝的宝\\测试目录"
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, dpath, True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()