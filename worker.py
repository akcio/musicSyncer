from threading import Thread
from queue import Queue
import os

class CheckThread(Thread):

    def __init__(self, pathToFolder, waitingQueue : Queue, pathToDatabase = None):
        super(CheckThread, self).__init__()
        self._pathToFolder = pathToFolder
        self._pathToDatabase = pathToDatabase
        self._newDirectories = waitingQueue

    @staticmethod
    def isFileMusic(path):
        import magic
        mimeType = magic.from_file(path, mime=True)
        if not mimeType.startswith("audio"):
            # print(path, mimeType)
            return False
        return True
        # return mimeType.startswith("audio")

    def isFileNew(self, path):
        # print("is music:", path)
        raise NotImplementedError

    def saveFile(self, path):
        raise NotImplementedError

    def run(self):
        print("Work in dir:", self._pathToFolder)
        itemsInFolder = os.listdir(self._pathToFolder)
        for item in itemsInFolder:
            itemPath = os.path.join(self._pathToFolder, item)
            if os.path.isdir(itemPath):
                self._newDirectories.put(itemPath)
                continue

            if self.isFileMusic(itemPath):
                continue

            if self.isFileNew(itemPath):
                self.saveFile(itemPath)
            else:
                # pass
                print("File:", itemPath, "already in collection")
