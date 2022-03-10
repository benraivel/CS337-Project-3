
import rbtree as rb

import process as p
import scheduler as s
import pandas as pd



def kernel(scheduler, max_arrival, processes = None, verbose = True, **kwargs):
    '''
    uses scheduler function to schedule processes and record statistics
    '''
    # initialize CPU, ready queue, waiting queue
    CPU = []
    ready = []
    waiting = []

    # if scheduler is CFS
    if scheduler is s.CF_scheduler:

        # ready is a RBTree
        ready = rb.RBTree()

    # if a list of processes isn't provided
    if processes == None:
        processes = [p.Process(0, [5, 1, 7], 0, 30),
                 p.Process(1, [4, 4, 2], 2, 35),
                 p.Process(2, [1, 6, 2], 5, 36),
                 p.Process(3, [6, 1, 5], 6, 20)]
    
    # set time to zero
    time = 0

    # move processes into ready queue
    s.add_ready(processes, ready, time)

    # loop while there are processes that have not finished
    while len(ready) > 0 or time < max_arrival or len(waiting) > 0:

        print(len(ready))

        # if no processes are ready
        if len(ready) == 0:

            # increment time
            time += 1

            # move newly arrived processes to ready queue
            s.add_ready(processes, ready, time)

            # move processes done with I/O back to ready
            s.manage_waiting(ready, waiting, time)

        # otherwise run the scheduler
        else:
            time = scheduler(processes, ready, waiting, CPU, time, verbose, **kwargs)

    # lists for wait and turnaround times
    wait_times = []
    turnaround_times = []
    response_times = []

    # loop over CPU
    for finished_process in CPU:

        # get PID of process
        PID = finished_process['process']

        # get process object
        process = processes[PID]

        # get wait and turnaround times
        wait_times.append(process.wait_time)
        turnaround_times.append(process.turnaround_time)
        response_times.append(process.response_time)

    # print avg wait and turnaround time
    print('avg. wait time: ' + str(sum(wait_times)/len(wait_times))
            + '\navg. turnaround time: ' + str(sum(turnaround_times)/len(turnaround_times))
            + '\navg. response time: ' + str(sum(response_times)/len(response_times)))
    
    # save data to csv
    df = pd.DataFrame(CPU)
    df.to_csv('results.csv', index=False)
    