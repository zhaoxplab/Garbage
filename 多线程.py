import threading
import time


exitFlag = 0

class my_thread(threading.Thread):
    def __init__(self, threadID, name, num):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.num = num

    def run(self):
        print(self.name + "...开始运行")
        put_time(self.name, self.num, 5)
        print(self.name + "...运行结束")


def put_time(threadName, delay, num):
    while num:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print(threadName, time.ctime())
        num -= 1


thread1 = my_thread(1, "thread_one", 1)
thread2 = my_thread(2, "thread_two", 2)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

print("over")
