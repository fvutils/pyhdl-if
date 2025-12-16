
import ctypes as ct
import hdl_if as hif
import asyncio
import time

@hif.api
class PerfBfm(object):
    """API for a simple BFM that does work consuming 1ns"""

    @hif.imp
    async def do_work(self) -> ct.c_uint32:
        """Do work (consumes 1ns in SV) and return call count"""
        pass

@hif.api
class PerfTest(object):
    """Performance test class comparing asyncio vs asyncio.to_thread"""

    @hif.exp
    async def run(self, bfm: ct.py_object):
        """Main test entry point called from SV"""
        num_calls_asyncio = 250000
        num_calls_thread = 25000
        
        print(f"[Py] Performance test: asyncio={num_calls_asyncio}, thread={num_calls_thread} Py->SV task calls", flush=True)
        print("=" * 60, flush=True)
        
        # Test 1: Pure asyncio sequential calls
        print(f"\n[Py] Test 1: Pure asyncio ({num_calls_asyncio} sequential calls)", flush=True)
        start_time = time.perf_counter()
        
        for i in range(num_calls_asyncio):
            await bfm.do_work()
        
        asyncio_time = time.perf_counter() - start_time
        asyncio_calls_per_sec = num_calls_asyncio / asyncio_time
        print(f"[Py] Asyncio: {asyncio_time:.4f}s, {asyncio_calls_per_sec:.1f} calls/sec", flush=True)
        
        # Test 2: asyncio.to_thread with run_coroutine_threadsafe
        print(f"\n[Py] Test 2: asyncio.to_thread ({num_calls_thread} calls from thread)", flush=True)
        
        loop = asyncio.get_event_loop()
        call_latencies = []
        
        def blocking_work():
            """Blocking work that runs in a thread and calls back to SV"""
            for i in range(num_calls_thread):
                call_start = time.perf_counter()
                future = asyncio.run_coroutine_threadsafe(
                    bfm.do_work(), loop)
                future.result(timeout=30.0)
                call_end = time.perf_counter()
                call_latencies.append(call_end - call_start)
            return num_calls_thread
        
        start_time = time.perf_counter()
        await asyncio.to_thread(blocking_work)
        thread_time = time.perf_counter() - start_time
        thread_calls_per_sec = num_calls_thread / thread_time
        
        # Analyze per-call latencies
        if call_latencies:
            avg_latency = sum(call_latencies) / len(call_latencies)
            min_latency = min(call_latencies)
            max_latency = max(call_latencies)
            print(f"[Py] Thread call latencies: avg={avg_latency*1000:.2f}ms, min={min_latency*1000:.2f}ms, max={max_latency*1000:.2f}ms", flush=True)
        
        print(f"[Py] Thread:  {thread_time:.4f}s, {thread_calls_per_sec:.1f} calls/sec", flush=True)
        
        # Summary
        print("\n" + "=" * 60, flush=True)
        print("[Py] Performance Summary:", flush=True)
        print(f"  Asyncio:        {asyncio_time:.4f}s ({asyncio_calls_per_sec:.1f} calls/sec)", flush=True)
        print(f"  Thread:         {thread_time:.4f}s ({thread_calls_per_sec:.1f} calls/sec)", flush=True)
        
        if thread_time > 0:
            ratio = asyncio_time / thread_time
            print(f"  Ratio (asyncio/thread): {ratio:.2f}x", flush=True)
        
        # Write results to file for test validation
        with open("perf_results.txt", "w") as fp:
            fp.write(f"asyncio_time={asyncio_time:.6f}\n")
            fp.write(f"asyncio_calls_per_sec={asyncio_calls_per_sec:.1f}\n")
            fp.write(f"thread_time={thread_time:.6f}\n")
            fp.write(f"thread_calls_per_sec={thread_calls_per_sec:.1f}\n")
            fp.write(f"num_calls_asyncio={num_calls_asyncio}\n")
            fp.write(f"num_calls_thread={num_calls_thread}\n")
            fp.write("status=PASS\n")
        
        print("[Py] TEST PASSED", flush=True)
