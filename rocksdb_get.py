import queue
import threading
import multiprocessing
import subprocess
import rocksdb
import random

db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))

q = queue.Queue()
for i in range(30): #put 30 tasks in the queue
    q.put(i)
random.randint(1,100000000)
def worker():
    while True:
        item = q.get()
        #execute a task: call a shell program and wait until it completes
        while True:
            batch = rocksdb.WriteBatch()
            for i in range(1000):
                batch.put(bytes(f"key{random.randint(1,100000000)}{random.randint(1,100000000)}", encoding="ascii"), bytes(f"Data{random.randint(1,100000000)}{random.randint(1,100000000)}", encoding="ascii"))
                db.write(batch)
        q.task_done()

cpus=multiprocessing.cpu_count() #detect number of cores
print("Creating %d threads" % cpus)
for i in range(cpus):
     t = threading.Thread(target=worker)
     t.daemon = True
     t.start()

q.join() #block until all tasks are done
