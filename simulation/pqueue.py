import heapq
from itertools import count
from numbers import Number
from typing import Generic, Tuple, TypeVar

T = TypeVar('T')


class PQueue(Generic[T]):
    """Priority queue using heapq.

    Allows insertion with priority, removing the first element from queue and
    increasing prioriry of an element.
    """

    def __init__(self):
        self._heap = list()
        self._dict = dict()
        self._count = count()

    def push(self, key: T, priority: Number = 0):
        """Enqueue a new key with given priority."""
        if key in self._dict:
            old = self._dict[key]
            num = old[1]
            old[2] = None
        else:
            num = next(self._count)

        entry = [priority, num, key]
        heapq.heappush(self._heap, entry)
        self._dict[key] = entry

    def pop(self) -> Tuple[T, Number]:
        """Remove the first element from the queue and return it."""
        key = None
        while key is None:
            priority, _, key = heapq.heappop(self._heap)
        del self._dict[key]

        return key, priority

    def pincr(self, key: T, priority: Number) -> bool:
        """Increase the priority of a key."""
        old = self._dict[key]
        if old[0] <= priority:
            return False

        num = old[1]
        old[2] = None

        entry = [priority, num, key]
        heapq.heappush(self._heap, entry)
        self._dict[key] = entry
        return True

    def count(self) -> int:
        """Return the number of elements of the priority queue."""
        return len(self._dict)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.pop()
        except IndexError:
            raise StopIteration()
