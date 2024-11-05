from .Scheduler import Scheduler

class RoundRobin(Scheduler):
    def __init__(self, processes, tcp, tip, tfp, quantum):
        super().__init__(processes, tcp, tip, tfp)
        self.quantum = quantum
        self.quantum_process = 0

    def select_next_process(self):
        # Implementación del Round Robin
        process = self.ready_queue.pop(0)
        return process  
    
    def preemptive(self):
        return self.process_running and self.quantum_process == self.quantum and not(self.current_process.remaining_time <= 0)

    def Simulate_running_to_ready(self):
        event = f"Time {self.current_time}: Process {self.current_process.name} expired his Quantum and moved to ready queue."
        print(event)  # Imprimir el evento antes de agregarlo
        self.events.append(event)
        self.process_running = False
        self.taken_cpu = False
        self.add_to_ready_queue(self.current_process)
        self.current_burst.finish = self.current_time
        self.current_process.add_burst(self.current_burst)
    
    def Simulate_TIP(self):
        super().Simulate_TIP()
        self.quantum_process = 0

    def Simulate_burst(self):
        super().Simulate_burst()
        self.quantum_process += 1



    