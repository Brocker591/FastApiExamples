import asyncio
import time

def blocking_task(n: int) -> int:
    time.sleep(n)
    return n

async def non_blocking_task(n: int) -> int:
    await asyncio.sleep(n)
    return n

#start_time = time.perf_counter()
#blocking_task(3)
#end_time = time.perf_counter()
#print(f"Blocking task hat {end_time - start_time} Sekunden benötigt")


async def main():
    start_time2 = time.perf_counter()
    await non_blocking_task(3)
    end_time2 = time.perf_counter()
    print(f"Non - Blocking task hat {end_time2 - start_time2} Sekunden benötigt")



#asyncio.run(main())

ones = [1] * 10

def blocking_function():
    results = []
    for n in ones:
        results.append(blocking_task(n))
    return results

async def non_blocking_function():
    results = []
    for n in ones:
        task = asyncio.create_task(non_blocking_task(n))
        results.append(task)
        return await asyncio.gather(*results)

start_time = time.perf_counter()
blocking_function()
end_time = time.perf_counter()
print(f"blocking function hat {end_time - start_time} Sekunden benötigt")

start_time2 = time.perf_counter()
asyncio.run(non_blocking_function())
end_time2 = time.perf_counter()
print(f"non_blocking_function hat {end_time2 - start_time2} Sekunden benötigt")