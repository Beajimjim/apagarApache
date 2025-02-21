import psutil
import time
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext

interval = 1
monitoring = False  # Variable para controlar el monitoreo

def stop_apache():
    try:
        result = subprocess.check_output(["tasklist"], universal_newlines=True)
        if "httpd.exe" in result:
            for line in result.splitlines():
                if "httpd.exe" in line:
                    pid = line.split()[1]
                    subprocess.run(["taskkill", "/PID", pid, "/F"], check=True)
                    log_message(f"Apache detenido con éxito. PID: {pid}")
                    return
        log_message("No se encontró ningún proceso de Apache ejecutándose.")
    except Exception as e:
        log_message(f"Error al detener Apache: {e}")

def get_network_usage(interval):
    initial_net_io = psutil.net_io_counters()
    time.sleep(interval)
    net_io = psutil.net_io_counters()
    subida = (net_io.bytes_sent - initial_net_io.bytes_sent) / interval
    descarga = (net_io.bytes_recv - initial_net_io.bytes_recv) / interval
    return subida, descarga

def log_message(message):
    text_area.insert(tk.END, message + "\n")
    text_area.see(tk.END)

def monitor_network():
    global monitoring
    if not monitoring:
        return
    
    log_message("Calculando valores normales...")
    total_subida, total_descarga = 0, 0
    for _ in range(20):
        s, d = get_network_usage(interval)
        total_subida += s
        total_descarga += d
    
    subida = total_subida / 20
    descarga = total_descarga / 20
    log_message(f"Valores normales: Subida={subida:.2f} bytes/s, Descarga={descarga:.2f} bytes/s")
    log_message("Comenzando monitoreo en tiempo real...")
    
    previous_net_io = psutil.net_io_counters()
    while monitoring:
        current_net_io = psutil.net_io_counters()
        nuevasubida = (current_net_io.bytes_sent - previous_net_io.bytes_sent) / interval
        nuevadescarga = (current_net_io.bytes_recv - previous_net_io.bytes_recv) / interval
        previous_net_io = current_net_io

        if nuevasubida > subida * 5 or nuevadescarga > descarga * 5:
            log_message(f"Anomalía detectada: Subida={nuevasubida:.2f} bytes/s, Descarga={nuevadescarga:.2f} bytes/s")
            log_message("Deteniendo Apache...")
            stop_apache()
            break
        else:
            log_message(f"Normal: Subida={nuevasubida:.2f} bytes/s, Descarga={nuevadescarga:.2f} bytes/s")
        
        time.sleep(interval)

def start_monitoring():
    global monitoring
    monitoring = True
    log_message("Iniciando monitoreo...")
    threading.Thread(target=monitor_network, daemon=True).start()

def stop_monitoring():
    global monitoring
    monitoring = False
    log_message("Monitoreo detenido.")

# Interfaz gráfica
root = tk.Tk()
root.title("Monitor de Red y Apache")
root.geometry("600x400")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
text_area.pack(pady=10)

start_button = tk.Button(root, text="Iniciar Monitoreo", command=start_monitoring)
start_button.pack()

stop_button = tk.Button(root, text="Detener Monitoreo", command=stop_monitoring)
stop_button.pack()

root.mainloop()
