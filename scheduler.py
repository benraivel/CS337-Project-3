# CS337 Project 2
# Ben Raivel
# process scheduling algorithm implementations

import process, rbtree


def FCFS_scheduler(processes, ready, CPU, time, verbose=True):
    '''
    first come first served scheduling algorithm
    '''
    # get process with lowest arrival
    current_process = find_lowest_arrival(ready)

    # set start time
    start_time = time

    # while burst time remains
    while(current_process.get_burst_time() > 0):

        # decrement burst time
        current_process.set_burst_time(current_process.get_burst_time()-1)

        # increment time
        time += 1

        # move newly arrived processes to ready queue
        add_ready(processes, ready, time)

    # set end time
    end_time = time

    # record process data to CPU list
    CPU.append(dict(process=current_process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=current_process.get_priority()))

    # set wait time and turnaround time
    current_process.wait_time = start_time - current_process.get_arrival_time()
    current_process.turnaround_time = current_process.wait_time + end_time - start_time

    # print process summary
    if(verbose):
        print('PID: ' + str(current_process.get_PID()) + 
            '\t[start, end]: [' + str(start_time) + ', ' + str(end_time) + ']' +
            '\twait : ' + str(current_process.wait_time) +
            '\tturnaround : ' + str(current_process.turnaround_time))

    return time

def SJF_scheduler(processes, ready, CPU, time, verbose=True):
    '''
    shortest job first scheduling algorithm
    '''
    # get shortest process
    current_process = find_shortest(ready)

    # set start time
    start_time = time

    # while burst time remains
    while(current_process.get_burst_time() > 0):

        #decrement burst time
        current_process.set_burst_time(current_process.get_burst_time()-1)

        # increment time
        time += 1

        # move newly arrived processes to ready queue
        add_ready(processes, ready, time)

    # set end time
    end_time = time
    
    # record process data to CPU list
    CPU.append(dict(process=current_process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=current_process.get_priority()))

    current_process.wait_time = start_time - current_process.get_arrival_time()

    current_process.turnaround_time = current_process.wait_time + end_time - start_time

    # print process summary
    if(verbose):
        print('PID: ' + str(current_process.get_PID()) + 
            '\t[start, end]: [' + str(start_time) + ', ' + str(end_time) + ']' +
            '\twait : ' + str(current_process.wait_time) +
            '\tturnaround : ' + str(current_process.turnaround_time))

    return time

def priority_scheduler(processes, ready, CPU, time, verbose=True):
    '''
    priority scheduling algorithm
    '''
    # get process with highest
    current_process = find_highest_priority(ready)

    # set start time
    start_time = time

    # while burst time remains
    while(current_process.get_burst_time() > 0):

        #decrement burst time
        current_process.set_burst_time(current_process.get_burst_time()-1)

        # increment time
        time += 1

        # move newly arrived processes to ready queue
        add_ready(processes, ready, time)

    # set end time
    end_time = time
    
    # add process data to CPU list
    CPU.append(dict(process=current_process.get_PID(),
                    start=start_time,
                    finish=end_time,
                    priority=current_process.get_priority()))

    current_process.wait_time = start_time - current_process.get_arrival_time()

    current_process.turnaround_time = current_process.wait_time + end_time - start_time

    # print process summary
    if(verbose):
        print('PID: ' + str(current_process.get_PID()) + 
                '\t[start, end]: [' + str(start_time) + ', ' + str(end_time) + ']' +
                '\twait : ' + str(current_process.wait_time) +
                '\tturnaround : ' + str(current_process.turnaround_time))

    return time

def RR_scheduler(processes, ready, waiting, CPU, time, verbose=True, **kwargs):
    '''
    round robin scheduler
    '''
    quantum = 2
    for key, val in kwargs.items():
        if key == 'quantum':
            quantum = val
    # get earliest arrival
    process = find_lowest_arrival(ready)

    # set start time
    start_time = time

     # if response time is None
    if process.response_time is None:
        
        # set to time
        process.response_time = start_time - process.get_arrival()

    # run process for one quantum
    for i in range(quantum):

        # decrement CPU
        process.get_duty()[0] -= 1

        # increment time
        time += 1

        # add newly arrived processes
        add_ready(processes, ready, time)

        # move processes done with I/O back to ready
        manage_waiting(ready, waiting, time)

        # if the process is finished with the CPU
        if process.get_duty()[0] < 1: break
        
    # set end time 
    end_time = time

    # record process data to CPU list
    CPU.append(dict(process=process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=process.get_priority()))

    # update waiting, turnaround times
    process.wait_time += start_time - process.get_arrival()
    process.turnaround_time += end_time - process.get_arrival()

    # print process summary
    if(verbose):
        print('PID: ' + str(process.get_PID())
                + ' | Burst: ' + str(process.get_duty()[0]) 
                + ' | start: ' + str(start_time) + ', end: ' + str(end_time) 
                + ' | wait : ' + str(process.wait_time)
                + ' | turnaround : ' + str(process.turnaround_time))


    # if the process is finished with the CPU
    if process.get_duty()[0] < 1:
        
        if len(process.get_duty()) > 1:
            waiting.append(process)

    else:
        # set new arrival time
        process.set_arrival(time)

        # add process back to ready
        ready.append(process)


    return time

def SRT_scheduler(processes, ready, waiting, CPU, time, verbose=True):
    '''
    shortest remaining time scheduler
    '''
    # find shortest process
    process = find_shortest(ready)

    # set start time
    start_time = time

    # if response time is None
    if process.response_time is None:
        
        # set to time first entered cpu - arrival time
        process.response_time = start_time - process.get_arrival()

    # while CPU burst time remains
    while(process.get_duty()[0] > 0):

        # run for one time slice
        process.get_duty()[0] -= 1

        time += 1

        # check for new arrivals
        new_arrived = add_ready(processes, ready, time)

        # move processes that are done waiting back to ready
        waiting_arrived = manage_waiting(ready, waiting, time)

        # interrupt if there are new jobs
        if new_arrived or waiting_arrived:

            # get shortest process in ready
            shortest_ready_process = find_shortest(ready)

            # if new process is shorter than remaining time
            if shortest_ready_process.get_duty()[0] < process.get_duty()[0]: 
                
                # put process back in ready queue
                ready.append(shortest_ready_process)

                # breake out of while loop
                break
            
            # put new process back in ready queue and continue current process
            ready.append(shortest_ready_process)

    # set end time
    end_time = time

    # record process data to CPU list
    CPU.append(dict(process=process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=process.get_priority()))

    # update waiting, turnaround times
    process.wait_time += start_time - process.get_arrival()
    process.turnaround_time += end_time - process.get_arrival()

    # print process summary
    if(verbose):
        print('PID: ' + str(process.get_PID())
                + ' | Burst: ' + str(process.get_duty()[0]) 
                + ' | start: ' + str(start_time) + ', end: ' + str(end_time) 
                + ' | wait : ' + str(process.wait_time)
                + ' | turnaround : ' + str(process.turnaround_time))


    # if the process is finished with the CPU
    if process.get_duty()[0] == 0:
        
        if len(process.get_duty()) > 1:

            process.set_waiting()
            waiting.append(process)
        
    else:
        # set new arrival time
        process.set_arrival(time)

        # add process back to ready
        ready.append(process)

    return time

def PP_scheduler(processes, ready, waiting, CPU, time, verbose=True):
    '''
    preemptive priority scheduler
    '''
    
    # find highest priority process
    process = find_highest_priority(ready)

    # set start time
    start_time = time

    # if response time is None
    if process.response_time is None:
        
        # set to time
        process.response_time = start_time - process.get_arrival()

    # while CPU burst time remains
    while(process.get_duty()[0] > 0):

        # run for one time slice
        process.get_duty()[0] -= 1

        time += 1

        # check for new arrivals
        new_arrived = add_ready(processes, ready, time)

        # move processes that are done waiting back to ready
        waiting_arrived = manage_waiting(ready, waiting, time)

        # interrupt if there is a higher priority job
        if new_arrived or waiting_arrived:

            # get highest priority process in ready
            highest_ready_process = find_highest_priority(ready)

            # if new process is higher priority than current
            if highest_ready_process.get_priority() > process.get_priority():

                # put process back in the ready queue
                ready.append(highest_ready_process)

                # break out of while loop
                break

            # put new process in ready queue and continue current process
            ready.append(highest_ready_process)

    # set end time 
    end_time = time

    # record process data to CPU list
    CPU.append(dict(process=process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=process.get_priority()))

    # update waiting, turnaround times
    process.wait_time += start_time - process.get_arrival()
    process.turnaround_time += end_time - process.get_arrival()

    # print process summary
    if(verbose):
        print('PID: ' + str(process.get_PID())
                + ' | Burst: ' + str(process.get_duty()[0]) 
                + ' | start: ' + str(start_time) + ', end: ' + str(end_time) 
                + ' | wait : ' + str(process.wait_time)
                + ' | turnaround : ' + str(process.turnaround_time))


    # if the process is finished with the CPU
    if process.get_duty()[0] == 0:
        
        if len(process.get_duty()) > 1:
            waiting.append(process)
        
    else:
        # set new arrival time
        process.set_arrival(time)

        # add process back to ready
        ready.append(process)

    return time

def CF_scheduler(processes, ready, waiting, CPU, time, verbose=True, **kwargs):
    '''
    completley fair scheduler using RBTree
    '''

    # default target latency
    target_latency = 5

    # check kwargs for target latency
    for key, val in kwargs.items():
        if key == 'target_latency':
            target_latency = val # update


    # get the process with the lowest vruntime
    process = ready.remove(node=ready.get_min())

    if process == None:

        return time+1
    
    # set start time
    start_time = time

    # if response time is None
    if process.response_time is None:
        
        # set to time first entered cpu - arrival time
        process.response_time = start_time - process.get_arrival()

    # compute dynamic quantum
    try:
        dynamic_quantum = target_latency/ready.get_size()
    except: 
        dynamic_quantum = 1

    if dynamic_quantum < 1: dynamic_quantum = 1

    for i in range(int(dynamic_quantum)):

        process.get_duty()[0] -= 1

        time += 1

        # add newly arrived processes
        add_ready(processes, ready, time)

        # move processes done with I/O back to ready
        manage_waiting(ready, waiting, time)

        # if the process is finished with the CPU
        if process.get_duty()[0] < 1: break
    
    # set end time 
    end_time = time

    process.increment_vruntime(end_time-start_time)

    # record process data to CPU list
    CPU.append(dict(process=process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=process.get_priority()))

    # update waiting, turnaround times
    process.wait_time += start_time - process.get_arrival()
    process.turnaround_time += end_time - process.get_arrival()

    # print process summary
    if(verbose):
        print('PID: ' + str(process.get_PID())
                + ' | Burst: ' + str(process.get_duty()[0]) 
                + ' | start: ' + str(start_time) + ', end: ' + str(end_time) 
                + ' | wait : ' + str(process.wait_time)
                + ' | turnaround : ' + str(process.turnaround_time))


    # if the process is finished with the CPU
    if process.get_duty()[0] < 1:
        
        if len(process.get_duty()) > 1:
            waiting.append(process)

    else:
        # set new arrival time
        process.set_arrival(time)

        # add process back to ready
        ready.insert(process.get_vruntime(), process)


    return time

def find_lowest_arrival(ready):
    '''
    returns earliest-arrived process in ready
    '''
    # index of lowest arrival in ready queue
    idx = 0

    # loop over ready queue
    for i in range(len(ready)):

        # if a lower value is encountered
        if(ready[i].get_arrival() < ready[idx].get_arrival()):
            idx = i
  
        # if an equally low value is encountered use PID to break tie
        elif(ready[i].get_arrival() == ready[idx].get_arrival()):
            
            # lower PID goes first
            if(ready[i].get_PID() < ready[idx].get_PID()):
                idx = i

    # remove and return lowest arrival
    return ready.pop(idx)

def find_shortest(ready):
    '''
    returns shortest-cpu-burst process in ready
    '''
    # index of shortest process
    idx = 0

    # loop over ready processes
    for i in range(len(ready)):
        
        # if next CPU burst is less than that of shortest
        if ready[i].get_duty()[0] < ready[idx].get_duty()[0]:

            # current process is new shortest
            idx = i

        # if they are equal
        elif ready[i].get_duty()[0] == ready[idx].get_duty()[0]:

            # resolve based on PID
            if ready[i].get_PID() < ready[idx].get_PID():

                # if PID is lower current process is new shortest
                idx = i

    # remove and return
    return ready.pop(idx)

def find_highest_priority(ready):
    '''
    returns highest priority process in ready
    '''
    # index of highest priority process
    idx = 0

    # loop over ready processes
    for i in range(len(ready)):
       
        # if the current process has higher priority
        if ready[i].get_priority() > ready[idx].get_priority():

            # current is new highest
            idx = i

        # if priority is equal
        elif ready[i].get_priority() == ready[idx].get_priority():

            # resolve using PID
            if ready[i].get_PID() < ready[idx].get_PID():

                # lower PID is chosen
                idx = i

    # remove and return
    return ready.pop(idx)

def add_ready(processes, ready, time):
    '''
    adds processes to ready at correct time
    '''
    # track if processes were added
    added = False

    # loop over processes
    for process in processes:

        # if process arrival is equal to time
        if process.get_arrival() == time:

            # if ready is a list
            if type(ready) == type([]):
            
                # add process to ready queue
                ready.append(process)
            
            else: # ready is RBTree
                ready.insert(process.get_vruntime(), process)

            # process was added
            added = True

    return added

def manage_waiting(ready, waiting, time):
    '''
    - decrements waiting time of processes in waiting 
    - moves processes that have finished I/O from waiting to ready
    '''
    # number of processes added
    added = False

    removed = 0

    # loop over waiting processes
    for i in range(len(waiting)):

        # if process is finished with I/O
        if waiting[i-removed].get_duty()[1] == 1:

            # remove process from waiting queue
            process = waiting.pop(i - removed)

            # increment removed
            removed += 1

            # slice the duty list 
            process.set_duty(process.get_duty()[2:])

            # set new arrival time
            process.set_arrival(time)

            # set process status to running
            process.set_running()
    
            # if ready is a list
            if type(ready) == type([]):
            
                # add process to ready queue
                ready.append(process)
            
            else: # ready is RBTree

                # add process to tree
                ready.insert(process.get_vruntime(), process)

            # process was added
            added = True
        
        # otherwise process stays in waiting
        else:

            # decrement waiting time in duty array
            waiting[i-removed].get_duty()[1] -= 1

    return added


def main():
    pass

if __name__ == '__main__':
    main()
