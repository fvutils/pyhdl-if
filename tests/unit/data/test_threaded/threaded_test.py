
import ctypes as ct
import hdl_if as hif
import threading
import asyncio

@hif.api
class Counter(object):
    """API for a simple counter in SystemVerilog"""

    @hif.imp
    async def increment(self) -> ct.c_uint32:
        """Increment counter and return new value"""
        print("-- counter.increment", flush=True)
        pass

    @hif.imp
    async def get_value(self) -> ct.c_uint32:
        """Get current counter value"""
        pass

@hif.api
class ThreadedTest(object):
    """Test class that demonstrates Python threads calling SV tasks"""

    @hif.exp
    async def run(self, counter : ct.py_object):
        """Main test entry point called from SV"""
        print("[Py] Starting threaded test", flush=True)
        
        # Test 1: Simple sequential calls
        print("[Py] Test 1: Sequential calls", flush=True)
        for i in range(3):
            print("--> await counter.increment", flush=True)
            val = await counter.increment()
            print("<-- await counter.increment", flush=True)
            print(f"[Py] Sequential increment {i+1}: counter = {val}", flush=True)
        
        # Test 2: Run blocking work in a thread using asyncio.to_thread
        print("[Py] Test 2: Thread-based calls using asyncio.to_thread", flush=True)
        
        results = []
        errors = []
        loop = asyncio.get_event_loop()
        
        def blocking_work():
            """Blocking work that runs in a thread and calls back to SV"""
            print("[Thread] Worker started", flush=True)
            try:
                for i in range(3):
                    # Schedule async call on the main event loop and wait for result
                    print("--> %d: threaded increment" % i, flush=True)
                    future = asyncio.run_coroutine_threadsafe(
                        counter.increment(), loop)
                    print("<-- %d: threaded increment" % i, flush=True)
                    val = future.result(timeout=30.0)
                    print(f"[Thread] Increment {i+1}: counter = {val}", flush=True)
                    results.append(val)
                print("[Thread] Worker completed successfully", flush=True)
            except Exception as e:
                import traceback
                print(f"[Thread] Error: {e}", flush=True)
                traceback.print_exc()
                errors.append(str(e))
            return results
        
        # Run the blocking work in a thread while keeping event loop active
        print("[Py] Test --> to_thread", flush=True)
        thread_results = await asyncio.to_thread(blocking_work)
        print("[Py] Test <-- to_thread", flush=True)
        
        print(f"[Py] Thread results: {thread_results}", flush=True)
        
        # Verify results
        final_val = await counter.get_value()
        print(f"[Py] Final counter value: {final_val}", flush=True)
        
        # Expected: 3 sequential + 3 threaded = 6
        expected = 6
        if final_val == expected and len(errors) == 0:
            print(f"[Py] TEST PASSED: counter = {final_val} (expected {expected})", flush=True)
            with open("status.txt", "w") as fp:
                fp.write("PASS: Threaded test completed successfully\n")
        else:
            print(f"[Py] TEST FAILED: counter = {final_val} (expected {expected}), errors = {errors}", flush=True)
            with open("status.txt", "w") as fp:
                fp.write(f"FAIL: counter = {final_val}, errors = {errors}\n")
