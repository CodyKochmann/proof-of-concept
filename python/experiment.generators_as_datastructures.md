## experiment - generators as datastructures

I had a hunch if I used a recursive coroutine as a read once singly linked list of windowed values, it would give me the behaviors of a simple dedicated data structure but run its operation way faster since its only reassigning variables as its internal mechanism. 

Once I got a working prototype I ran some benchmarks. For large windows, due to recursion eventually biting back, deque is still faster for window generation. For smaller windows, streaming values to this blows deque benchmarks out of the water :)

```python
def window(current, *following):
    if following:
        next_window = window(*following)
        first = yield (current, *next_window.send(None))
        while 1:
            _ = yield (first, *next_window.send(current))
            current = first
            first = _
    else:
        while 1:
            current = yield (current,)
            
if __name__ == '__main__':
    w=window(*range(3))
    print(w)
    print(w.send(None))
    print(w.send(8))
    print(w.send(11))
    print(w.send(50))
    for i in range(50):
        print(w.send(i))
``` 
