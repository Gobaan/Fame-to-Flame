import threading
class Log():
    def __init__(self, filename):
        self.log = open(filename, 'a')
        self.lock = threading.Lock()
       
    def write(self, line):
        self.lock.acquire()
        self.log.write(line)
        self.log.flush()
        self.lock.release()

    def writelines(self, line):
        self.lock.acquire()
        self.log.writelines(line)
        self.log.flush()
        self.lock.release()
    
    def close(self):
        self.lock.acquire()
        del logs[self.log.name]
        self.log.close()
        self.lock.release()

logs = {}
lock = threading.Lock()
def GetLog(filename):
    if filename not in logs:
        lock.acquire() 
        if filename not in logs:
            logs[filename] = Log(filename)
        lock.release() 
    return logs[filename]
