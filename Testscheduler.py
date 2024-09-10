from Process import Process
from FCFS import FCFS
from RoundRobin import RoundRobin
from PriorityScheduler import PriorityScheduler
from SPN import SPN
from SRTN import SRTN
import json

# Crear instancias de procesos para probar los algoritmos
def load_processes_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        processes = [
            Process(
                name=process_data['name'],
                arrival_time=process_data['arrival_time'],
                cpu_bursts=process_data['cpu_bursts'],
                burst_duration=process_data['burst_duration'],
                io_duration=process_data['io_duration'],
                priority=process_data['priority']
            )
            for process_data in data
        ]
    return processes


# Agrupar los procesos en una lista
processes_set_1 = load_processes_from_json('process_set/set_1.json')
processes_set_2 = load_processes_from_json('process_set/set_2.json')
processes_set_3 = load_processes_from_json('process_set/set_3.json')
processes_set_4 = load_processes_from_json('process_set/set_4.json')

processes = processes_set_1

# Crear una instancia de FCFS Scheduler
tcp_fcfs = 0 # Tiempo de conmutación entre procesos para FCFS
tip_fcfs = 0  # Tiempo de inicialización del proceso en FCFS
tfp_fcfs = 0  # Tiempo de finalización del proceso en FCFS

fcfs_scheduler = FCFS(processes=processes, tcp=tcp_fcfs, tip=tip_fcfs, tfp=tfp_fcfs)

# Crear una instancia de Round Robin Scheduler
tcp_rr = 1  # Tiempo de conmutación entre procesos para Round Robin
tip_rr = 2  # Tiempo de inicialización del proceso en Round Robin
tfp_rr = 1  # Tiempo de finalización del proceso en Round Robin
quantum_rr = 4  # Quantum para Round Robin

rr_scheduler = RoundRobin(processes=processes, tcp=tcp_rr, tip=tip_rr, tfp=tfp_rr, quantum=quantum_rr)

tcp_p = 1  # Tiempo de conmutación entre procesos para Priority
tip_p = 2  # Tiempo de inicialización del proceso en Priority
tfp_p = 1  # Tiempo de finalización del proceso en Priority

priority_scheduler = PriorityScheduler(processes=processes, tcp=tcp_p, tip=tip_p, tfp=tfp_p)

# Crear una instancia de SPN Scheduler
tcp_spn = 1  # Tiempo de conmutación entre procesos para SPN
tip_spn = 2  # Tiempo de inicialización del proceso en SPN
tfp_spn = 1  # Tiempo de finalización del proceso en SPN

spn_scheduler = SPN(processes=processes, tcp=tcp_spn, tip=tip_spn, tfp=tfp_spn)

# Crear una instancia de SRTN Scheduler
tcp_srtn = 1  # Tiempo de conmutación entre procesos para SRTN
tip_srtn = 2  # Tiempo de inicialización del proceso en SRTN
tfp_srtn = 1  # Tiempo de finalización del proceso en SRTN

srtn_scheduler = SRTN(processes=processes, tcp=tcp_srtn, tip=tip_srtn, tfp=tfp_srtn)

events_fcfs = fcfs_scheduler.run()
events_rr = rr_scheduler.run()
events_priority = priority_scheduler.run()
events_spn = spn_scheduler.run()
events_srtn = srtn_scheduler.run()

fcfs_scheduler.save_events_to_file(events_fcfs, 'resultados/simulation_fcfs_results.txt')
rr_scheduler.save_events_to_file(events_rr, 'resultados/simulation_rr_results.txt')
priority_scheduler.save_events_to_file(events_priority, 'resultados/simulation_priority_results.txt')
spn_scheduler.save_events_to_file(events_spn, 'resultados/simulation_spn_results.txt')
srtn_scheduler.save_events_to_file(events_srtn, 'resultados/simulation_srtn_results.txt')