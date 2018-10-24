from worker import CheckThread
import os
from queue import Queue

if __name__ == '__main__':
    mainDir = "/home/ileaban/Загрузки"
    waitProcess = Queue()
    waitProcess.put(mainDir)

    while not waitProcess.empty():
        try:
            data = waitProcess.get_nowait()
        except:
            continue
        if os.path.isdir(data):
            newThread = CheckThread(data, waitProcess)
            newThread.run()

    # for item in os.listdir(mainDir):
    #     if os.path.isdir(os.path.join(mainDir ,item)):
    #         newThread = CheckThread(os.path.join(mainDir , item), waitProcess)
    #         newThread.run()