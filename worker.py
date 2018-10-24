from threading import Thread
import os

class CheckTrhead(Thread):

    def __init__(self, pathToFolder, pathToDatabase):
        super(CheckTrhead, self).__init__()
        self._pathToFolder = pathToFolder
        self._pathToDatabase = pathToDatabase
        self._newDirectories = []

    def isFileNew(self, path):
        raise NotImplementedError

    def saveFile(self, path):
        raise NotImplementedError

    def run(self):
        itemsInFolder = os.listdir(self._pathToFolder)
        for item in itemsInFolder:
            if os.path.isdir(item):
                self._newDirectories.append(item)
                continue
            if self.isFileNew(item):
