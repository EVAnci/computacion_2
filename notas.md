See [this](https://docs.python.org/3/library/asyncio-task.html) 

```python
In [3]: import asyncio
   ...: import time
   ...: from datetime import datetime
   ...: 
   ...: async def say_after(delay, what):
   ...:     await asyncio.sleep(delay)
   ...:     print(what)
   ...: 
   ...: async def main():
   ...:     start = datetime.now()
   ...:     print(f"started at {time.strftime('%S')}")
   ...: 
   ...:     await say_after(1, 'hello')
   ...:     await say_after(2, 'world')
   ...: 
   ...:     end = datetime.now()
   ...:     print(f"finished at {time.strftime('%S')}. Diff: {end-start}")
   ...: 
   ...: asyncio.run(main())
started at 42
hello
world
finished at 45. Diff: 0:00:03.003713

In [4]: import asyncio
   ...: import time
   ...: from datetime import datetime
   ...: 
   ...: async def say_after(delay, what):
   ...:     await asyncio.sleep(delay)
   ...:     print(what)
   ...: 
   ...: async def main():
   ...:     start = datetime.now()
   ...:     print(f"started at {time.strftime('%S')}")
   ...: 
   ...:     task1 = asyncio.create_task(
   ...:         say_after(1, 'hello')
   ...:     )
   ...:     task2 = asyncio.create_task(
   ...:         say_after(2, 'world')
   ...:     )
   ...: 
   ...:     await task1
   ...:     await task2
   ...: 
   ...:     end = datetime.now()
   ...:     print(f"finished at {time.strftime('%S')}. Diff: {end-start}")
   ...: 
   ...: asyncio.run(main())
started at 31
hello
world
finished at 33. Diff: 0:00:02.001824
```
