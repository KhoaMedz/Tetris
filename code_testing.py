import Shapes, random, Piece, Board
from queue import Queue
  
# Initializing a queue
q = Queue(maxsize = 5)
  
# Adding of element to queue
for i in range(q.maxsize):
    q.put(i)

for i in q.queue:
    print(i, end=' ')