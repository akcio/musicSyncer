from threading import Thread
from queue import Queue
import os
from ffmpeg.stream import Stream
import hashlib

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
    @staticmethod
    def checkInDataBase(fileHash):
        import sqlite3
        conn = sqlite3.connect("files.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT file_path FROM files WHERE file_hash = ?""", [(str(fileHash))])
        data = cursor.fetchone()
        if data != None:
            print(data)
            return True
        else:
            cursor.execute("""INSERT INTO files(file_path, file_hash) VALUES (?, ?)""", [str("test"), str(fileHash)])
            conn.commit()
        return False

    def isFileNew(self, path):
        file = open(path, 'rb')
        hasher = hashlib.sha256(file.read())
        # hasher.update(bytes())
        file.close()
        newFileHash = hasher.hexdigest() # (file.readlines())
        if (self.checkInDataBase(newFileHash)):
            pass
        # print("is music:", path)
        return True
        raise NotImplementedError

    def saveFile(self, path):
        return False
        raise NotImplementedError

    def run(self):
        print("Work in dir:", self._pathToFolder)
        itemsInFolder = os.listdir(self._pathToFolder)
        for item in itemsInFolder:
            itemPath = os.path.join(self._pathToFolder, item)
            if os.path.isdir(itemPath):
                self._newDirectories.put(itemPath)
                continue

            if not self.isFileMusic(itemPath):
                continue

            if self.isFileNew(itemPath):
                self.saveFile(itemPath)
            else:
                # pass
                print("File:", itemPath, "already in collection")
