#!/usr/bin/env python3
import time
import os
import subprocess
def measure_time(script=[], init_script=[], prerun_script=[], postrun_script=[], final_script=[], iteration=20, silent=False):
    if len(init_script) > 0:
        if silent:
            subprocess.call(init_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.call(init_script)
 
    i = 0
    timestamps = []
    while i < iteration:
        if len(prerun_script) > 0:
            if silent:
                subprocess.call(prerun_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                subprocess.call(prerun_script)

        start_time = time.time()
        if silent:
            subprocess.call(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.call(script)
        end_time = time.time()
        timestamps.append(end_time - start_time)

        if len(postrun_script) > 0:
            if silent:
                subprocess.call(postrun_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                subprocess.call(postrun_script)
        i += 1
    timestamp = sum(timestamps) / float(len(timestamps))

    if len(final_script) > 0:
        if silent:
            subprocess.call(final_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.call(final_script)
    return timestamp

iteration = 20
t0 = measure_time(script=["./compile_gcc.sh"], init_script=["make", "clean"], postrun_script=["make", "clean"], iteration=iteration)
t1 = measure_time(script=["./compile_rvpc.sh"], postrun_script=["make", "clean"], iteration=iteration)
t2 = measure_time(script=["./run_gcc.sh"], init_script=["./compile_gcc.sh"], final_script=["make", "clean"], iteration=iteration)
t3 = measure_time(script=["./run_rvpc_no_trace.sh"], init_script=["./compile_rvpc.sh"], final_script=["make", "clean"], iteration=iteration)
t4 = measure_time(script=["./run_rvpc_trace.sh"], init_script=["./compile_rvpc.sh"], prerun_script=["rm", "-rf", "./trace"], final_script=["make", "clean"], iteration=iteration)
print("Performance measurement - " + str(iteration) + " iterations")
print("GCC - Compile time (second/iter): " + str(t0))
print("RVPC - Compile time (second/iter): " + str(t1))
print("--------------")
print("GCC - Execution time (second/iter): " + str(t2))
print("RVPC - no analysis, tracing to /dev/null - Execution time (second/iter): " + str(t3))
print("RVPC - no analysis, tracing to ./trace   - Execution time (second/iter): " + str(t4))