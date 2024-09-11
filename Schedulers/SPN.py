from .Scheduler import Scheduler

class SPN(Scheduler):
    def select_next_process(self):
        # Selección del proceso con la ráfaga más corta
        return self.ready_queue.pop(0)
    
    def add_to_ready_queue(self, process):
        self.ready_queue.append(process)
        self.ready_queue.sort(key=lambda p: p.burst_duration)
    
    def run(self):
        # Mantener un registro de los eventos (simulación de un logger básico)
        while self.processes or self.ready_queue or self.waiting_queue or self.process_running:
        
            # 1. Verificar si el proceso en running puede terminar (De Running a Terminado)        
            if self.process_running and self.current_process.remaining_time <= 0:
                self.Simulate_running_to_finish()
            # 2. Verificar si el proceso en running tiene que bloquearse (De Running a Bloqueado)
            elif self.process_running and self.current_process.remaining_time > 0 and self.burst_time == 0:
                self.Simulate_running_to_blocked()

            # 3. Verificar si el proceso en running pierde el procesador (De Running a Listo)
            # En SPN no ocurre porque es non-preemptive, entonces esta parte no aplica.

            # 4. Verificar si algún proceso bloqueado puede cambiar a listo (Bloqueado a Listo)
            self.Simulate_blocked_to_ready()

            #Actualizo el contador de sus tiempo en ready
            self.Update_ready_time()

            # 5. Verificar si algún proceso puede entrar al sistema (Nuevo a Listo)
            self.Simulate_new_to_ready()

            # 6. Verificar si un proceso en listo puede despacharse (De Listo a Running)
            if not self.process_running and self.ready_queue:
                self.Simulate_ready_to_running()

            # Simulación del TIP (Tiempo de Inicialización)
            if self.process_running and self.init_time < self.tip:
                self.Simulate_TIP()
        
            # Si se completó el TIP, comienza la ejecución de la ráfaga de CPU
            if self.process_running and self.init_time == self.tip and not(self.taken_cpu):
                self.Simulate_end_TIP()

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

