from Scheduler import Scheduler

class FCFS(Scheduler):
    def select_next_process(self):
        # Selección del primer proceso en la cola
        return self.ready_queue.pop(0)
    
    def run(self):
        while self.processes or self.ready_queue or self.waiting_queue or self.process_running:
        
            # 1. Verificar si el proceso en running puede terminar (De Running a Terminado)        
            if self.process_running and self.current_process.remaining_time <= 0:
                if self.finish_time == self.tfp:  # Simular el TFP (Tiempo de finalización)
                    self.current_process.self.finish_time = self.current_time
                    self.current_process.turnaround_time = self.current_time - self.current_process.arrival_time
                    self.current_process.normalized_turnaround_time = self.current_process.turnaround_time / self.current_process.service_time
                    event = f"Time {self.current_time}: Process {self.current_process.name} completed."
                    print(event)  # Imprimir el evento antes de agregarlo
                    self.events.append(event)
                    self.taken_cpu = False
                    self.process_running = False  # Proceso terminó, liberar la CPU
                    self.finish_time = 0
                    self.switch_time = 0
                    self.burst_time = 0
                else:
                    self.finish_time += 1  # Simular el tiempo de finalización (TFP)
            # 2. Verificar si el proceso en running tiene que bloquearse (De Running a Bloqueado)
            elif self.process_running and self.current_process.remaining_time > 0 and self.burst_time == 0:
                if self.switch_time == self.tcp:
                    # Mover el proceso a la waiting_queue para simular I/O
                    event = f"Time {self.current_time}: Process {self.current_process.name} moved to waiting queue (I/O)."
                    print(event)  # Imprimir el evento antes de agregarlo
                    self.events.append(event)
                    self.add_to_waiting_queue(self.current_process)
                    self.process_running = False  # Bloquear el proceso
                    self.taken_cpu = False
                    self.switch_time = 0
                else:
                    self.switch_time += 1  # Simular el TCP (Tiempo de conmutación)

            # 3. Verificar si el proceso en running pierde el procesador (De Running a Listo)
            # En FCFS no ocurre porque es non-preemptive, entonces esta parte no aplica.

            # 4. Verificar si algún proceso bloqueado puede cambiar a listo (Bloqueado a Listo)
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

            # 5. Verificar si algún proceso puede entrar al sistema (Nuevo a Listo)
            for process in list(self.processes):
                if process.arrival_time <= self.current_time:
                    self.add_to_ready_queue(process)
                    self.processes.remove(process)
                    event = f"Time {self.current_time}: Process {process.name} added to ready queue."
                    print(event)  # Imprimir el evento antes de agregarlo
                    self.events.append(event)

            # 6. Verificar si un proceso en listo puede despacharse (De Listo a Running)
            if not self.process_running and self.ready_queue:
                self.current_process = self.select_next_process()
                self.process_running = True
                self.init_time = 0  # Reiniciar el contador de TIP (Tiempo de Inicialización)
                event = f"Time {self.current_time}: Process {self.current_process.name} dispatched to running."
                print(event)  # Imprimir el evento antes de agregarlo
                self.events.append(event)

            # Simulación del TIP (Tiempo de Inicialización)
            if self.process_running and self.init_time < self.tip:
                self.init_time += 1  # Incrementar el tiempo de inicialización
                event = f"Time {self.current_time}: Process {self.current_process.name} initialization TIP in progress ({self.init_time}/{self.tip})."
                print(event)  # Imprimir el evento antes de agregarlo
                self.events.append(event)
        
            # Si se completó el TIP, comienza la ejecución de la ráfaga de CPU
            if self.process_running and self.init_time == self.tip and not(self.taken_cpu):
                self.burst_time = self.current_process.burst_duration  # Establecer la ráfaga actual del proceso
                self.taken_cpu = True
                event = f"Time {self.current_time}: Process {self.current_process.name} started execution after TIP."
                print(event)  # Imprimir el evento antes de agregarlo
                self.events.append(event)

            # Simulación de ejecución del proceso
            if self.taken_cpu and self.process_running and self.burst_time > 0 and self.init_time == self.tip:
                self.burst_time = self.burst_time - 1
                self.current_process.remaining_time -= 1
                event = f"Time {self.current_time}: Process {self.current_process.name} running. {self.burst_time} ms left."
                print(event)  # Imprimir el evento antes de agregarlo
                self.events.append(event)
        
            # Avanza el tiempo de la simulación
            self.current_time += 1  
        # Generar un resumen de la simulación (puedes exportar esto a un archivo si lo deseas)
        return self.events

    
