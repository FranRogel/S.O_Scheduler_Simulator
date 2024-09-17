from .Scheduler import Scheduler

class SPN(Scheduler):
    def select_next_process(self):
        # Selección del proceso con la ráfaga más corta
        return self.ready_queue.pop(0)
    
    def add_to_ready_queue(self, process):
        self.ready_queue.append(process)
        self.ready_queue.sort(key=lambda p: p.burst_duration)

