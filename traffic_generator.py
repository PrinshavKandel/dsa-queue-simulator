class MaxHeap:
    def __init__(self):
        self.h = []

    def push(self, x):
        self.h.append(x)
        i = len(self.h) - 1
        while i > 0:
            p = (i - 1) // 2
            if self.h[p] >= self.h[i]:
                break
            self.h[p], self.h[i] = self.h[i], self.h[p]
            i = p

    def pop(self):
        if not self.h:
            return None
        self.h[0], self.h[-1] = self.h[-1], self.h[0]
        val = self.h.pop()
        i = 0
        n = len(self.h)

        while True:
            l = 2*i + 1
            r = 2*i + 2
            largest = i

            if l < n and self.h[l] > self.h[largest]:
                largest = l
            if r < n and self.h[r] > self.h[largest]:
                largest = r
            if largest == i:
                break

            self.h[i], self.h[largest] = self.h[largest], self.h[i]
            i = largest

        return val

    