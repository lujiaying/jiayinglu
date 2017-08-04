# coding: utf-8

import heapq

class minHeap():

    def __init__(self, k):
        self._k = k
        self._heap = []

    def add(self, item):
        if len(self._heap) < self._k:
            self._heap.append(item)
            heapq.heapify(self._heap)
        else:
            if item > self._heap[0]:
                self._heap[0] = item
                heapq.heapify(self._heap)

    def get_min(self):
        return self._heap[0]

    def get_all(self):
        return self._heap

if __name__ == '__main__':
    import random
    min_heap = minHeap(5)
    for i in xrange(15):
        e = random.randint(0, 100)
        min_heap.add(e)
        print('add [%d], min_heap:%s' % (e, min_heap.get_all()))
