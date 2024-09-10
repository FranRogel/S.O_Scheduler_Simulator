class Process:
    def __init__(self, name, arrival_time, cpu_bursts, burst_duration, io_duration, priority):
        self.name = name
        self.arrival_time = arrival_time #Momento en que debera ser creado el proceso
        self.burst_duration = burst_duration #Cuando dura su cpu burst normalmente (en ms)
        self.service_time = cpu_bursts * burst_duration #Tiempo que estar en servicio el proceso
        self.io_duration = io_duration #Cuanto dura su interrumpción de entrada/salida (en ms)
        self.priority = priority #Prioridad en caso de necesitarla
        self.remaining_time = cpu_bursts * burst_duration #Tiempo que le queda al proceso para terminarseo
        self.waiting_time = 0 #Tiempo que estuvo el proceso en estado de espera
        self.burst_remaining = burst_duration #Tiempo que le queda a su burst
        self.turnaround_time = 0 #Tiempo de Retorno
        self.normalized_turnaround_time = 0 #Tiempo de Retorno normalizado
    
    def __str__(self):
        return f"Process(name={self.name})"
