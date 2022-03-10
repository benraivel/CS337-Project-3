# CS337 Project 3
# Ben Raivel

# Process class

class Process:

    def __init__(self, PID, duty, arrival_time, priority):
        '''
        init process with PID, burst time, arrival time, and proiority
        '''
        # initialize with attributes provided as parameters
        self.PID = PID
        self.duty = duty
        self.arrival_time = arrival_time
        self.priority = priority

        # attributes for cfs
        self.vruntime = 0
        self.weight = 5

        # set wait time, turnaround time, and response time to zero
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = None

        self.status = 'running'
        self.queue = 0

    def __str__(self):
        return 'P' + str(self.PID) + '{status: ' + self.status + ' | wait: ' + str(self.wait_time) + '}'

    # getter and setter methods for process
    def get_PID(self):
        return self.PID

    def get_duty(self):
        return self.duty

    def set_duty(self, duty):
        self.duty = duty

    def get_arrival(self):
        return self.arrival_time

    def set_arrival(self, arrival):
        self.arrival_time = arrival

    def get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def get_status(self):
        return self.status

    def set_running(self):
        self.status = 'running'

    def set_waiting(self):
        self.status = 'waiting'

    def get_queue(self):
        return self.queue

    def set_queue(self, queue):
        self.queue = queue

    def get_vruntime(self):
        return self.vruntime

    def increment_vruntime(self, time):
        self.vruntime += time*self.weight

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight
