import psutil
import tkinter as tk
from tkinter import ttk
import threading

def update_progress():
    memory_usage = psutil.virtual_memory().percent
    print(memory_usage)
    memory_progress = memory_usage / 100.0
    memory_canvas.itemconfig(progress_arc_memory, extent=-360 * memory_progress)

    cpu_usage = psutil.cpu_percent()
    print(cpu_usage)
    cpu_progress = cpu_usage / 100.0
    cpu_canvas.itemconfig(progress_arc_cpu, extent=-360 * cpu_progress)

    root.after(1000, update_progress)

def monitor_resource_usage():
    update_thread = threading.Thread(target=update_progress)
    update_thread.daemon = True
    update_thread.start()

root = tk.Tk()
root.title("Resource Monitor")

memory_canvas = tk.Canvas(root, width=200, height=200)
memory_canvas.pack(padx=20, pady=20)

cpu_canvas = tk.Canvas(root, width=200, height=200)
cpu_canvas.pack(padx=20, pady=20)

progress_arc_memory = memory_canvas.create_arc(
    50, 50, 150, 150,
    style=tk.ARC,
    start=90,
    outline="gray",
    width=10
)

progress_arc_cpu = cpu_canvas.create_arc(
    50, 50, 150, 150,
    style=tk.ARC,
    start=90,
    outline="gray",
    width=10
)

monitor_resource_usage()

root.mainloop()
