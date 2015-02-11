# encoding: utf-8

import threading
import thread
import time

# 此为最简单的例子
'''
# 方法1: 将要执行的方法作为参数传给Thread的构造方法
def func():
    print 'func() passed to Thread'

t = threading.Thread(target=func)
t.start()


# 方法2: 从Thread继承，并重写run()
class MyThread(threading.Thread):
    def run(self):
        print 'MyThread extended from Thread'

t = MyThread()
t.start()
'''

# join的应用
'''
def context(tJoin):
    print 'in threadContext.'
    tJoin.start()

    # 将阻塞tContext直到threadJoin终止
    tJoin.join()

    # tJoin终止后继续执行
    print 'out threadContext.'


def join():
    print 'in threadJoin.'
    time.sleep(1)
    print 'out threadJoin.'


tJoin = threading.Thread(target=join)
tContext = threading.Thread(target=context, args=(tJoin,))

tContext.start()
'''

'''
# lock的应用
data = 8
lock = threading.Lock()

def func():
    #global data
    print '%s acquire lock...' % threading.currentThread().getName()

    # 调用acquire([timeout])时，线程将一直阻塞，
    # 直到获得锁定或者直到timeout秒后（timeout参数可选）
    # 返回是否获得锁
    if lock.acquire():
        print '%s get lock...' % threading.currentThread().getName()
        #data += 1
        print data
        time.sleep(2)
        print '%s release lock...' % threading.currentThread().getName()

        # 调用release()将释放锁
        lock.release()

t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t3 = threading.Thread(target=func)
t1.start()
t2.start()
t3.start()
'''

# 为线程定义一个函数
def print_time(thread_name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" %(thread_name, time.ctime(time.time()))


if __name__ == '__main__':
    # 创建两个线程
    try:
        thread.start_new_thread(print_time, ('Thread-1', 2))
        thread.start_new_thread(print_time, ('Thread-2', 4))
    except:
        print 'Error, unable to start thread'

    while 1:
        pass
