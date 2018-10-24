from threading import Thread
from queue import Queue
import os

class CheckThread(Thread):

    def __init__(self, pathToFolder, waitingQueue : Queue, pathToDatabase = None):
        super(CheckThread, self).__init__()
        self._pathToFolder = pathToFolder
        self._pathToDatabase = pathToDatabase
        self._newDirectories = waitingQueue

    def isFileNew(self, path):
        # print("Not implemented")
        return True
        raise NotImplementedError

    def saveFile(self, path):
        # print("Not implemented")
        return True
        raise NotImplementedError

    def run(self):
        print("Work in dir:", self._pathToFolder)
        itemsInFolder = os.listdir(self._pathToFolder)
        for item in itemsInFolder:
            if os.path.isdir(os.path.join(self._pathToFolder, item)):
                self._newDirectories.put(os.path.join(self._pathToFolder, item))
                continue
            if self.isFileNew(item):
                self.saveFile(item)
            else:
                print("File:", item, "already in collection")
