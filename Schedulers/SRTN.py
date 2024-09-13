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


    def run(self):
        # Mantener un registro de los eventos (simulación de un logger básico)
        while self.processes or self.ready_queue or self.waiting_queue or self.process_running:
            # 1. Verificar si el proceso en running puede terminar (De Running a Terminado)                
            if self.process_running and self.current_process.remaining_time <= 0:
                self.Simulate_running_to_finish()
            # 2. Verificar si el proceso en running tiene que bloquearse (De Running a Bloqueado)
            elif self.process_running and self.current_process.remaining_time > 0 and self.burst_time == 0 and self.taken_cpu:
                    self.Simulate_running_to_blocked()
            # 3. Verificar si el proceso en running pierde el procesador (De Running a Listo)
            elif self.process_running and self.ready_queue and self.next_process_short_burst_remaining():
                event = f"Time {self.current_time}: Process {self.current_process.name}: lost the processor because a process with lower burst appeared."
                print(event)  # Imprimir el evento antes de agregarlo
                self.events.append(event)
                self.process_running = False 
                self.taken_cpu = False
                self.current_process.burst_remaining = self.burst_time
                self.current_burst.finish = self.current_time
                self.current_process.add_burst(self.current_burst)
                self.add_to_ready_queue(self.current_process)

            # 4. Verificar si algún proceso bloqueado puede cambiar a listo (Bloqueado a Listo)
            self.Simulate_blocked_to_ready()

            # 5. Verificar si algún proceso puede entrar al sistema (Nuevo a Listo)
            self.Simulate_new_to_ready()

            #Actualizo el contador de sus tiempo en ready
            self.Update_ready_time()

            # 6. Verificar si un proceso en listo puede despacharse (De Listo a Running)
            if not self.process_running and self.ready_queue:
                self.Simulate_ready_to_running()

            # Simulación del TIP (Tiempo de Inicialización)

            # Simulación del TIP (Tiempo de Inicialización)
            if self.process_running and self.init_time < self.tip:
                self.Simulate_TIP()

            # Si se completó el TIP, comienza la ejecución de la ráfaga de CPU
            if self.process_running and self.init_time == self.tip and not(self.taken_cpu):
                self.Simulate_end_TIP()
                self.burst_time = self.current_process.burst_remaining  # Establecer la ráfaga actual del proceso

            # Simulación de ejecución del proceso
            if self.taken_cpu and self.process_running and self.burst_time > 0 and self.init_time == self.tip:
                self.Simulate_burst()

            #Comprobar si la cpu esta inutil
            if not self.ready_queue and not self.process_running:
                event = f"Time {self.current_time}: CPU Not Busy"
                self.events.append(event)
                self.not_busy_cpu_time += 1

            # Avanza el tiempo de la simulación
            self.current_time += 1 

        # Generar un resumen de la simulación 
        total_return_time = self.current_time
        num_processes = len(self.finish_queu)
        average_return_time = sum(process.turnaround_time for process in self.finish_queu) / num_processes
        event = f"Tiempo de Retorno de la Tanda: {total_return_time:.2f} ||| Tiempo de Retorno Normalizado: {average_return_time:.2f}"
        self.events.append(event)
        # Datos sobre el uso del CPU
        cpu_so_time = self.so_time
        not_busy_cpu = self.not_busy_cpu_time
        event = f"Tiempo del CPU ocupado por el SO: {cpu_so_time}"
        self.events.append(event)
        event = f"Tiempo del CPU desocupado: {not_busy_cpu}"
        self.events.append(event)
        return self.events