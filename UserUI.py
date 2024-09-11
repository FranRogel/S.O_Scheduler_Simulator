import tkinter as tk
from tkinter import ttk
from Schedulers.FCFS import FCFS
from Schedulers.RoundRobin import RoundRobin
from Schedulers.PriorityScheduler import PriorityScheduler
from Schedulers.SPN import SPN
from Schedulers.SRTN import SRTN
from Process import Process
import matplotlib.pyplot as plt
from GanttGrafic import *
import sys
import os
import json


# Crear una clase para manejar la interfaz gráfica y la simulación
class DispatcherSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dispatcher Simulator")

        # Variables de simulación
        self.scheduler_type = tk.StringVar(value="FCFS")
        self.selected_process_set = tk.StringVar(value="Set 1")
        self.tcp = tk.DoubleVar(value=0)
        self.tip = tk.DoubleVar(value=0)
        self.tfp = tk.DoubleVar(value=0)
        self.quantum = tk.DoubleVar(value=0)

        #Cargar los set de procesos
        self.processes_set_1 = self.load_processes_from_json('process_set/set_1.json')
        self.processes_set_2 = self.load_processes_from_json('process_set/set_2.json')
        self.processes_set_3 = self.load_processes_from_json('process_set/set_3.json')
        self.processes_set_4 = self.load_processes_from_json('process_set/set_4.json')

        # Crear los elementos de la interfaz
        self.create_widgets()
        # Inicializar ventanas
        self.graph_window = None 
        self.events_window = None

    def create_widgets(self):
        # Selector de tipo de scheduler
        ttk.Label(self.root, text="Tipo de Scheduler:").grid(row=0, column=0, padx=5, pady=5)
        scheduler_menu = ttk.Combobox(self.root, textvariable=self.scheduler_type)
        scheduler_menu['values'] = ("FCFS", "Round Robin", "SPN", "SRTN", "Priority")
        scheduler_menu.grid(row=0, column=1, padx=5, pady=5)
        scheduler_menu.bind("<<ComboboxSelected>>", self.on_scheduler_selected)  # Evento para detectar cambios

        # Selector del set de procesos
        ttk.Label(self.root, text="Set de Procesos:").grid(row=1, column=0, padx=5, pady=5)
        process_set_menu = ttk.Combobox(self.root, textvariable=self.selected_process_set)
        process_set_menu['values'] = ("Set 1", "Set 2", "Set 3", "Set 4")  # Añadir los sets de procesos
        process_set_menu.grid(row=1, column=1, padx=5, pady=5)

        # Entradas para TCP, TIP, TFP
        ttk.Label(self.root, text="TCP:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.tcp).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="TIP:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.tip).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="TFP:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.tfp).grid(row=4, column=1, padx=5, pady=5)

        # Entrada para Quantum (inicialmente oculta)
        self.quantum_label = ttk.Label(self.root, text="Quantum:")
        self.quantum_entry = ttk.Entry(self.root, textvariable=self.quantum)

        # Botón de Simular
        self.simulate_button = ttk.Button(self.root, text="Simular", command=self.simulate)
        self.simulate_button.grid(row=6, column=0, columnspan=2, pady=10)

    def on_scheduler_selected(self, event):
        """Muestra u oculta la entrada para quantum según el tipo de scheduler seleccionado."""
        scheduler_type = self.scheduler_type.get()
        if scheduler_type == "Round Robin":
            self.quantum_label.grid(row=5, column=0, padx=5, pady=5)  # Mostrar label de Quantum
            self.quantum_entry.grid(row=5, column=1, padx=5, pady=5)  # Mostrar entry de Quantum
        else:
            self.quantum_label.grid_forget()  # Ocultar label de Quantum
            self.quantum_entry.grid_forget()  # Ocultar entry de Quantum

    def simulate(self):
        # Si ya hay una ventana de gráfico abierta, cerrarla
        if self.graph_window:
            self.graph_window.destroy()

        # Obtener los parámetros ingresados
        scheduler_type = self.scheduler_type.get()
        tcp_value = self.tcp.get()
        tip_value = self.tip.get()
        tfp_value = self.tfp.get()
        set = self.selected_process_set.get()
        quantum_value = self.quantum.get()
        
        processes_set = self.get_proccesses_set(set)
        # Crear instancia del Scheduler según el tipo seleccionado
        scheduler = self.create_scheduler(scheduler_type, tcp_value, tip_value, tfp_value, quantum_value,processes_set)
        
        # Ejecutar la simulación
        events = scheduler.run()

        # Crear una nueva ventana para los eventos
        self.events_window = tk.Toplevel(self.root)
        self.events_window.title("Eventos de la Simulación")
    
        # Crear un widget ScrolledText para mostrar los eventos
        self.events_text = tk.Text(self.events_window, wrap=tk.WORD)
        self.events_text.pack(expand=1, fill=tk.BOTH)
    
        # Insertar los eventos en el widget
        for event in events:
            self.events_text.insert(tk.END, event + '\n')
    
        # Hacer que el widget sea de solo lectura
        self.events_text.config(state=tk.DISABLED)
    
        # Crear una nueva ventana para el gráfico de Gantt
        self.graph_window = tk.Toplevel(self.root)
        self.graph_window.title("Resultados de la Simulación")

        processes = scheduler.finish_queu
        limit = scheduler.current_time
        # Crear una nueva ventana para el gráfico de Gantt
        self.graph_window = tk.Toplevel(self.root)
        self.graph_window.title("Resultados de la Simulación")

        # Mostrar el gráfico en la ventana
        plot_gantt_chart(processes, limit)

    def create_scheduler(self, scheduler_type, tcp, tip, tfp, quantum, cloned_processes):
        # Aquí eliges el tipo de scheduler y creas la instancia adecuada
        if scheduler_type == "FCFS":
            return FCFS(cloned_processes, tcp, tip, tfp)
        elif scheduler_type == "Round Robin":
            return RoundRobin(cloned_processes, tcp, tip, tfp, quantum)
        elif scheduler_type == "SPN":
            return SPN(cloned_processes, tcp, tip, tfp)
        elif scheduler_type == "Priority":
            return PriorityScheduler(cloned_processes, tcp, tip, tfp)
        elif scheduler_type == "SRTN":
            return SRTN(cloned_processes, tcp, tip, tfp)
        else:    
            raise ValueError("Tipo de Scheduler no soportado")
    
    def get_proccesses_set(self, set_name):
        set = []
        if set_name == "Set 1":
            for p in self.processes_set_1:
                print(p)
                set.append(p.clone())
            return set
        elif set_name == "Set 2":
            for p in self.processes_set_2:
                set.append(p.clone())
            return set  
        elif set_name == "Set 3":
            for p in self.processes_set_3:
                set.append(p.clone())
            return set 
        elif set_name == "Set 4":
            for p in self.processes_set_4:
                set.append(p.clone())
            return set  
        else:
            raise ValueError(f"Unknown process set: {set_name}")

    def resource_path(self,relative_path):
    #Obtener la ruta absoluta al archivo, ya sea en el directorio de trabajo actual o dentro del archivo ejecutable
        try:
            # PyInstaller crea una carpeta temporal y coloca el archivo ejecutable en ella
            base_path = sys._MEIPASS
        except AttributeError:
            # PyInstaller no está ejecutando, se utiliza la ruta del script
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)
    
    def load_processes_from_json(self,file_path):
        json_path = self.resource_path(file_path)
        print(f"Looking for file at: {json_path}")  # Debug print to check file path
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"File not found: {json_path}")
        with open(json_path, 'r') as file:
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


# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = DispatcherSimulatorApp(root)
    root.mainloop()