from Scheduler import Scheduler

class SPN(Scheduler):
    def select_next_process(self):
        # Selección del proceso con la ráfaga más corta
        return self.ready_queue.pop(0)
    
    def add_to_ready_queue(self, process):
        self.ready_queue.append(process)
        self.ready_queue.sort(key=lambda p: p.burst_duration)
    
    def run(self):
        # Mantener un registro de los eventos (simulación de un logger básico)
        events = []
        process_running = False
        current_process = None
        burst_time = 0
        switch_time = 0
        finish_time = 0
        init_time = 0  
        taken_cpu = False

        while self.processes or self.ready_queue or self.waiting_queue or process_running:
        
            # 1. Verificar si el proceso en running puede terminar (De Running a Terminado)        
            if process_running and current_process.remaining_time <= 0:
                if finish_time == self.tfp:  # Simular el TFP (Tiempo de finalización)
                    current_process.finish_time = self.current_time
                    current_process.turnaround_time = self.current_time - current_process.arrival_time
                    current_process.normalized_turnaround_time = current_process.turnaround_time / current_process.service_time
                    event = f"Time {self.current_time}: Process {current_process.name} completed."
                    print(event)  # Imprimir el evento antes de agregarlo
                    events.append(event)
                    process_running = False  # Proceso terminó, liberar la CPU
                    finish_time = 0
                    switch_time = 0
                    burst_time = 0
                else:
                    finish_time += 1  # Simular el tiempo de finalización (TFP)
            # 2. Verificar si el proceso en running tiene que bloquearse (De Running a Bloqueado)
            elif process_running and current_process.remaining_time > 0 and burst_time == 0:
                if switch_time == self.tcp:
                    # Mover el proceso a la waiting_queue para simular I/O
                    event = f"Time {self.current_time}: Process {current_process.name} moved to waiting queue (I/O)."
                    print(event)  # Imprimir el evento antes de agregarlo
                    events.append(event)
                    self.add_to_waiting_queue(current_process)
                    process_running = False  # Bloquear el proceso
                    taken_cpu = False
                    switch_time = 0
                else:
                    switch_time += 1  # Simular el TCP (Tiempo de conmutación)

            # 3. Verificar si el proceso en running pierde el procesador (De Running a Listo)
            # En SPN no ocurre porque es non-preemptive, entonces esta parte no aplica.

            # 4. Verificar si algún proceso bloqueado puede cambiar a listo (Bloqueado a Listo)
            for process in list(self.waiting_queue):
                if process.waiting_time >= process.io_duration:
                    self.add_to_ready_queue(process)
                    self.waiting_queue.remove(process)
                    process.waiting_time = 0
                    event = f"Time {self.current_time}: Process {process.name} added back to ready queue."
                    print(event)  # Imprimir el evento antes de agregarlo
                    events.append(event)
                else:
                    process.waiting_time += 1

            # 5. Verificar si algún proceso puede entrar al sistema (Nuevo a Listo)
            for process in list(self.processes):
                if process.arrival_time <= self.current_time:
                    self.add_to_ready_queue(process)
                    self.processes.remove(process)
                    event = f"Time {self.current_time}: Process {process.name} added to ready queue."
                    print(event)  # Imprimir el evento antes de agregarlo
                    events.append(event)

            # 6. Verificar si un proceso en listo puede despacharse (De Listo a Running)
            if not process_running and self.ready_queue:
                current_process = self.select_next_process()
                process_running = True
                init_time = 0  # Reiniciar el contador de TIP (Tiempo de Inicialización)
                event = f"Time {self.current_time}: Process {current_process.name} dispatched to running."
                print(event)  # Imprimir el evento antes de agregarlo
                events.append(event)

            # Simulación del TIP (Tiempo de Inicialización)
            if process_running and init_time < self.tip:
                init_time += 1  # Incrementar el tiempo de inicialización
                event = f"Time {self.current_time}: Process {current_process.name} initialization TIP in progress ({init_time}/{self.tip})."
                print(event)  # Imprimir el evento antes de agregarlo
                events.append(event)
        
            # Si se completó el TIP, comienza la ejecución de la ráfaga de CPU
            if process_running and init_time == self.tip and not(taken_cpu):
                burst_time = current_process.burst_duration  # Establecer la ráfaga actual del proceso
                taken_cpu = True
                event = f"Time {self.current_time}: Process {current_process.name} started execution after TIP."
                print(event)  # Imprimir el evento antes de agregarlo
                events.append(event)

            # Simulación de ejecución del proceso
            if taken_cpu and process_running and burst_time > 0 and init_time == self.tip:
                burst_time = burst_time - 1
                current_process.remaining_time -= 1
                event = f"Time {self.current_time}: Process {current_process.name} running. {burst_time} ms left."
                print(event)  # Imprimir el evento antes de agregarlo
                events.append(event)
        
            # Avanza el tiempo de la simulación
            self.current_time += 1  
        # Generar un resumen de la simulación (puedes exportar esto a un archivo si lo deseas)
        return events

