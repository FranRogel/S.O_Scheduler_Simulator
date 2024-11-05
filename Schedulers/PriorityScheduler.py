from .Scheduler import Scheduler

class PriorityScheduler(Scheduler):

    def select_next_process(self):
        # Selección del proceso con mayor prioridad
        self.ready_queue.sort(key=lambda p: p.priority)
        return self.ready_queue.pop(0)

    def next_process_high_priority(self):
        # Selección del proceso con mayor prioridad
        self.ready_queue.sort(key=lambda p: p.priority)
        process = self.ready_queue[0]
        return process.priority < self.current_process.priority
    
    def preemptive(self):
        return self.process_running and self.ready_queue and self.next_process_high_priority() and not(self.current_process.remaining_time <= 0) and not(self.burst_time == 0)

    def Simulate_running_to_ready(self):
        event = f"Time {self.current_time}: Process {self.current_process.name}: lost the processor because a process with higher priority appeared."
        print(event)  # Imprimir el evento antes de agregarlo
        self.events.append(event)
        self.process_running = False 
        self.taken_cpu = False
        self.add_to_ready_queue(self.current_process)
        self.current_burst.finish = self.current_time
        self.current_process.add_burst(self.current_burst)
