from GanttGrafic import Burstline
import bisect

class Scheduler:
    def __init__(self, processes, tcp, tip, tfp):
        self.processes = processes
        self.new_queue = []
        self.ready_queue = []
        self.waiting_queue = []
        self.finish_queu = []
        self.current_time = 0
        self.tcp = tcp  # Tiempo de conmutación entre procesos
        self.tip = tip  # Tiempo de inicialización del proceso
        self.tfp = tfp  # Tiempo de finalización del proceso
        self.so_time = 0
        self.not_busy_cpu_time = 0 #Tiempo de la CPU sin estar ocupada
        #Otras variables para la simulacion
        self.events = []
        self.process_running = False
        self.current_process = None
        self.current_burst = None
        self.burst_time = None
        self.switch_time = 0
        self.finish_time = 0
        self.init_time = 0  
        self.taken_cpu = False

    def add_to_new_queue(self,process):
        self.new_queue.append(process)
    
    def add_to_ready_queue(self, process):
        self.ready_queue.append(process)

    def add_to_waiting_queue(self,process):
        self.waiting_queue.append(process)

    def add_to_finish_queu(self, process):
        # Extraemos solo los nombres de los procesos que ya están en la cola
        process_names = [p.name for p in self.finish_queu]
        # Usamos bisect para encontrar la posición donde insertar el nuevo proceso de forma ordenada
        position = bisect.bisect(process_names, process.name)
        # Insertamos el proceso en la posición correcta
        self.finish_queu.insert(position, process)

    def end_report(self):
        for process in self.finish_queu:
            print(process)

    def select_next_process(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    def Simulate_running_to_finish(self):
        if self.finish_time == self.tfp:  # Simular el TFP (Tiempo de finalización)
            self.current_process.finish_time = self.current_time
            self.current_process.turnaround_time = self.current_time - self.current_process.arrival_time
            self.current_process.normalized_turnaround_time = self.current_process.turnaround_time / self.current_process.service_time
            self.current_burst.tfp_time = self.current_time - self.tfp
            self.current_burst.finish = self.current_time
            self.current_process.add_burst(self.current_burst)
            self.add_to_finish_queu(self.current_process)
            event = f"Time {self.current_time}: Process {self.current_process.name} completed."
            print(event)  # Imprimir el evento antes de agregarlo
            self.events.append(event)
            self.taken_cpu = False
            self.process_running = False  # Proceso terminó, liberar la CPU
            self.finish_time = 0
            self.switch_time = 0
            self.burst_time = 0
        else:
            self.Update_so_time()
            self.finish_time += 1  # Simular el tiempo de finalización (TFP)
            event = f"Time {self.current_time}: Process {self.current_process.name} started finish {self.finish_time}."
            print(event)
            self.events.append(event)

    def Simulate_running_to_blocked(self):
        if self.switch_time == self.tcp:
            # Mover el proceso a la waiting_queue para simular I/O
            event = f"Time {self.current_time}: Process {self.current_process.name} moved to waiting queue (I/O)."
            print(event)  # Imprimir el evento antes de agregarlo
            self.events.append(event)
            self.current_burst.tcp_time = self.current_time - self.tcp
            self.current_burst.finish = self.current_time
            self.current_process.add_burst(self.current_burst)
            self.add_to_waiting_queue(self.current_process)
            self.process_running = False  # Bloquear el proceso
            self.taken_cpu = False
            self.switch_time = 0
        else:  
            event = f"Time {self.current_time}: Process {self.current_process.name} started moved to waiting queue (I/O) ({self.switch_time}/{self.tcp})."
            print(event)
            self.events.append(event)
            self.Update_so_time()
            self.switch_time += 1  # Simular el TCP (Tiempo de conmutación)
    
    def Simulate_blocked_to_ready(self):
        for process in list(self.waiting_queue):
            if process.waiting_time >= process.io_duration:
                self.add_to_ready_queue(process)
                self.waiting_queue.remove(process)
                process.waiting_time = 0
                event = f"Time {self.current_time}: Process {process.name} added back to ready queue."
                print(event)  # Imprimir el evento antes de agregarlo
                self.events.append(event)
            else:
                process.waiting_time += 1

    def Simulate_new_to_ready(self):
        for process in list(self.processes):
            if process.arrival_time <= self.current_time:
                self.add_to_ready_queue(process)
                self.processes.remove(process)
                event = f"Time {self.current_time}: Process {process.name} added to ready queue."
                print(event)  # Imprimir el evento antes de agregarlo
                self.events.append(event)

    def Simulate_ready_to_running(self):
        self.current_process = self.select_next_process()
        self.process_running = True
        self.init_time = 0  # Reiniciar el contador de TIP (Tiempo de Inicialización)
        event = f"Time {self.current_time}: Process {self.current_process.name} dispatched to running."
        print(event)  # Imprimir el evento antes de agregarlo
        self.events.append(event)
 
    def Update_ready_time(self):
        for process in self.ready_queue:
            process.ready_time += 1

    def Update_so_time(self):
        self.so_time += 1
    
    def Simulate_TIP(self):
        # Simulación del TIP (Tiempo de Inicialización)
        self.init_time += 1  # Incrementar el tiempo de inicialización
        self.Update_so_time()
        event = f"Time {self.current_time}: Process {self.current_process.name} initialization TIP in progress ({self.init_time}/{self.tip})."
        print(event)  # Imprimir el evento antes de agregarlo
        self.events.append(event)

    def Simulate_end_TIP(self):    
        # Si se completó el TIP, comienza la ejecución de la ráfaga de CPU
        self.burst_time = self.current_process.burst_duration  # Establecer la ráfaga actual del proceso
        self.taken_cpu = True
        self.current_burst = Burstline(self.current_time)
        event = f"Time {self.current_time}: Process {self.current_process.name} started execution after TIP."
        print(event)  # Imprimir el evento antes de agregarlo
        self.events.append(event)
    
    def Simulate_burst(self):
        self.burst_time = self.burst_time - 1
        self.current_process.remaining_time -= 1
        event = f"Time {self.current_time}: Process {self.current_process.name} running. {self.burst_time} ms left."
        print(event)  # Imprimir el evento antes de agregarlo
        self.events.append(event)
   
    def run(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    def Save_events_to_file(self, events, filename):
        with open(filename, 'w') as file:
            for event in events:
                file.write(f"{event}\n")

