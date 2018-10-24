from worker import CheckThread
import os
from queue import Queue

def createDatabase():
    import sqlite3
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS files (file_path text, file_hash text);""")
    conn.commit()

if __name__ == '__main__':
    mainDir = "/home/ileaban/Загрузки"
    mainDir = "/home/ileaban/PycharmProjects/lab1/festival/"
    waitProcess = Queue()
    waitProcess.put(mainDir)
    createDatabase()

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