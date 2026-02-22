class Array: 
    def __init__(self, size):
        if size <= 0:
            raise ValueError("Size harus > 0")
        self._size = size
        self._data = [None] * size

    def length(self):
        return self._size

    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index di luar batas")
        return self._data[index]

    def __setitem__(self, index, value):
        if index < 0 or index >= self._size:
            raise IndexError("Index di luar batas")
        self._data[index] = value

    def clear(self, value):
        for i in range(self._size):
            self._data[i] = value

    def __iter__(self):
        return iter(self._data)