from .Scheduler import Scheduler

class FCFS(Scheduler):
    def select_next_process(self):
        # Selección del primer proceso en la cola
        return self.ready_queue.pop(0)