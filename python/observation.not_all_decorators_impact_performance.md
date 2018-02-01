## observation - not all decorators impact performance

Decorators are pretty well known to impact performance, but do all do this?

Apparently not.

```python
(py3) ~ $ i
Python 3.6.1 (default, Apr  4 2017, 09:40:21)
Type 'copyright', 'credits' or 'license' for more information
IPython 6.1.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from generators import rps

In [2]: def add():
   ...:     return 1+2
   ...:

In [3]: rps(add)
Out[3]: 3080651

In [4]: rps(add)
Out[4]: 3074790

In [5]: rps(add)
Out[5]: 2990402

In [6]: def add():
   ...:     ret = 1+2
   ...:     return ret
   ...:

In [7]: rps(add)
Out[7]: 3001072

In [8]: rps(add)
Out[8]: 2883338

In [9]: rps(add)
Out[9]: 2928027

In [10]: def add():
    ...:     return 1+2
    ...:

In [11]: from functools import wraps

In [12]: def wrapped(fn):
    ...:     @wraps(fn)
    ...:     def wrapper(*a, **k):
    ...:         return fn(*a, **k)
    ...:     return wrapper
    ...:

In [13]: @wrapped
    ...: def add():
    ...:     return 1+2
    ...:

In [14]: rps(add)
Out[14]: 1700739

In [15]: rps(add)
Out[15]: 1729304

In [16]: rps(add)
Out[16]: 1707205

In [17]: @wrapped
    ...: @wrapped
    ...: def add():
    ...:     return 1+2
    ...:

In [18]: rps(add)
Out[18]: 1244947

In [19]: rps(add)
Out[19]: 1256726

In [20]: rps(add)
Out[20]: 1255845

In [21]: def wrapped(fn):
    ...:     @wraps(fn)
    ...:     def wrapper():
    ...:         return fn()
    ...:     return wrapper
    ...:

In [22]: #@wrapped
    ...: def add():
    ...:     return 1+2
    ...:

In [23]: rps(add)
Out[23]: 3081086

In [24]: rps(add)
Out[24]: 2978758

In [25]: rps(add)
Out[25]: 3061717

In [26]: @wrapped
    ...: def add():
    ...:     return 1+2
    ...:

In [27]: rps(add)
Out[27]: 2198937

In [28]: rps(add)
Out[28]: 2219667

In [29]: rps(add)
Out[29]: 2070476

In [30]: #@wrapped
    ...: def add(a=1, b=2):
    ...:     return a+b
    ...:

In [31]: rps(add)
Out[31]: 2706172

In [32]: rps(add)
Out[32]: 2729120

In [33]: rps(add)
Out[33]: 2647500

In [34]: #@wrapped
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [35]: rps(add)
Out[35]: 2533974

In [36]: rps(add)
Out[36]: 2592301

In [37]: rps(add)
Out[37]: 2605995

In [38]: @wrapped
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [39]: rps(add)
Out[39]: 1887516

In [40]: rps(add)
Out[40]: 1955626

In [41]: rps(add)
Out[41]: 1886427

In [42]: def wrapped(fn):
    ...:     @wraps(fn)
    ...:     def wrapper():
    ...:         ret = fn()
    ...:         return ret
    ...:     return wrapper
    ...:

In [43]: @wrapped
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [44]: rps(add)
Out[44]: 1845714

In [45]: rps(add)
Out[45]: 1836440

In [46]: rps(add)
Out[46]: 1840607

In [47]: def wrapped(fn):
    ...:     return wraps(fn)(lambda:fn())
    ...:

In [48]: @wrapped
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [49]: rps(add)
Out[49]: 1958741

In [50]: rps(add)
Out[50]: 1886333

In [51]: rps(add)
Out[51]: 1920940

In [52]: def wrapped(fn):
    ...:     return lambda:fn()
    ...:

In [53]: @wrapped
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [54]: rps(add)
Out[54]: 1918134

In [55]: rps(add)
Out[55]: 1951910

In [56]: rps(add)
Out[56]: 1865480

In [57]: @wrapped
    ...: @wrapped
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [58]: rps(add)
Out[58]: 1579737

In [59]: rps(add)
Out[59]: 1601820

In [60]: rps(add)
Out[60]: 1590539

In [61]: @wrapped
    ...: @wrapped
    ...: @wrapped
    ...: @wrapped
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [62]: rps(add)
Out[62]: 1089920

In [63]: rps(add)
Out[63]: 1099779

In [64]: rps(add)
Out[64]: 1097965

In [65]: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [66]: rps(add)
Out[66]: 2614041

In [67]: rps(add)
Out[67]: 2594044

In [68]: rps(add)
Out[68]: 2571581

In [69]: from strict_functions import noglobals

In [70]: @noglobals
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [71]: rps(add)
Out[71]: 2631203

In [72]: rps(add)
Out[72]: 2530266

In [73]: rps(add)
Out[73]: 2382588

In [74]: @noglobals
    ...: @noglobals
    ...: @noglobals
    ...: @noglobals
    ...: def add():
    ...:     a=1
    ...:     b=2
    ...:     return a+b
    ...:

In [75]: rps(add)
Out[75]: 2625384

In [76]: rps(add)
Out[76]: 2612208

In [77]: rps(add)
Out[77]: 2607033
```
