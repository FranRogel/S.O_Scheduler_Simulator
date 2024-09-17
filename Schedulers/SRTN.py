from .Scheduler import Scheduler

class SRTN(Scheduler):
    def select_next_process(self):
        # Selección del proceso con el tiempo restante más corto
        return self.ready_queue.pop(0)
    
    def add_to_ready_queue(self, process):
        self.ready_queue.append(process)
        self.ready_queue.sort(key=lambda p: p.burst_remaining)

    def next_process_short_burst_remaining(self):
        process = self.ready_queue[0]
        return process.burst_remaining < self.burst_time

    def preemptive(self):
        return self.process_running and self.ready_queue and self.next_process_short_burst_remaining()
    
    def Simulate_running_to_blocked(self):
        if self.switch_time == self.tcp:
            # Mover el proceso a la waiting_queue para simular I/O
            event = f"Time {self.current_time}: Process {self.current_process.name} moved to waiting queue (I/O)."
            print(event)  # Imprimir el evento antes de agregarlo
            self.events.append(event)
            self.add_to_waiting_queue(self.current_process)
            self.current_process.burst_remaining = self.current_process.burst_duration
            self.current_burst.tcp_time = self.current_time - self.tcp
            self.current_burst.finish = self.current_time
            self.current_process.add_burst(self.current_burst)
            self.process_running = False  # Bloquear el proceso
            self.taken_cpu = False
            self.switch_time = 0
        else:
            self.switch_time += 1  # Simular el TCP (Tiempo de conmutación)

