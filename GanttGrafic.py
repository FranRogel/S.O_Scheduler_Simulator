import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Burstline():
    def __init__(self, start):
        self.start = start
        self.tfp_time = 0
        self.tcp_time = 0
        self.finish = 0

    def set_finish(self, finish):
        self.finish = finish

    def both_zero(self):
        return self.tcp_time == 0 and self.tfp_time == 0
    
    def length(self):
        if self.tfp_time == self.finish or self.tcp_time == self.finish or self.both_zero():
            return self.finish - self.start
        elif self.tfp_time > 0:
            return self.tfp_time - self.start
        else:
            return self.tcp_time - self.start

def plot_gantt_chart(processes, finish, graph_window=None):
    fig, (gnt, info) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})

    if graph_window:
        plt.close(graph_window)
    
    # Ajustes básicos del gráfico de Gantt
    gnt.set_xlabel('Tiempo')
    gnt.set_ylabel('Procesos')

    # Nombres de los procesos (en el eje Y)
    process_names = [process.name for process in processes]
    gnt.set_yticks([i + 1 for i in range(len(processes))])
    gnt.set_yticklabels(process_names)

    # Tamaño del eje Y, más espacio entre los procesos
    gnt.set_ylim(0.5, len(processes) + 0.5)

    # Ajustar los límites del tiempo (eje X)
    gnt.set_xlim(0, finish)
    
    # Para cada proceso, agregamos sus bursts al gráfico
    for i, process in enumerate(processes):
        for burst in process.burst_history:
            start_time = burst.start
            if burst.tfp_time > 0:
                active_duration = burst.tfp_time 
            elif burst.tcp_time > 0:
                active_duration = burst.tcp_time 
            else:
                active_duration = burst.finish 
            
            inactive_duration = burst.finish - active_duration
            leng_burst = burst.length()
            
            # Barra para el tiempo activo
            gnt.barh(i + 1, leng_burst , left=start_time, color='lightgreen', edgecolor='black', height=0.4)
            
            gnt.barh(i + 1, inactive_duration, left=active_duration, color='lightcoral', edgecolor='black', height=0.4)

    # Ajustes para el gráfico de información de los procesos
    info.axis('off')  # Ocultar el eje

    # Preparar la tabla de información
    table_data = []
    for process in sorted(processes, key=lambda p: p.name):
        table_data.append([
            process.name,
            f"Tiempo de retorno: {process.turnaround_time}",
            f"Tiempo Medio de Retorno: {process.normalized_turnaround_time:.2f}",
            f"Tiempo en Estado de Listo: {process.ready_time:}",
            f"Tiempo de Servicio: {process.service_time}"  # Columna agregada
        ])
    
    # Mostrar la tabla en el gráfico de información
    table = plt.table(cellText=table_data,
                      colLabels=['Proceso', 'Tiempo de retorno', 'Tiempo Medio de Retorno', 'Tiempo en Estado de Listo', 'Tiempo de Servicio'],
                      cellLoc='left',
                      loc='center',
                      bbox=[0.0, 0.0, 1.0, 1.0],
                      colColours=['#f2f2f2']*5,  # Se agrega un color para la nueva columna
                      cellColours=[['#ffffff']*5 for _ in range(len(table_data))])  # Se ajusta a 5 columnas
    
    # Ajustar el tamaño de la fuente
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.5, 1.5)  # Escalar la tabla (ancho, alto)

    plt.subplots_adjust(hspace=0.4)  # Ajustar espacio entre los gráficos
    plt.show()
    return fig








