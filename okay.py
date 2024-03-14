import psutil
import tkinter as tk
from tkinter import ttk
import time

# Function to get CPU information
def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)  # Get CPU usage percentage
    cpu_freq = psutil.cpu_freq()  # Get CPU frequency
    cpu_info = {
        "CPU Percent": cpu_percent,
        "CPU Frequency (MHz)": cpu_freq.current
    }
    return cpu_info

# Function to get memory information
def get_memory_info():
    mem = psutil.virtual_memory()  # Get virtual memory usage
    memory_info = {
        "Total Memory (MB)": mem.total // (1024 * 1024),
        "Used Memory (MB)": mem.used // (1024 * 1024),
        "Memory Percent": mem.percent
    }
    return memory_info

# Function to get information about running processes
def get_running_processes():
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            process_info = process.info
            process_name = process.name()
            process_username = process.username()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        processes.append({
            'pid': process_info['pid'],
            'name': process_name,
            'username': process_username,
            'cpu_percent': process_info['cpu_percent'],
            'memory_percent': process_info['memory_percent']
        })
    return processes

# Function to update system information label
def update_system_info_label():
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    
    # Update label text with CPU and memory information
    system_info_label.config(text=f"CPU Percent: {cpu_info['CPU Percent']}%\n"
                                   f"Total Memory: {memory_info['Total Memory (MB)']} MB\n"
                                   f"Used Memory: {memory_info['Used Memory (MB)']} MB\n"
                                   f"Memory Percent: {memory_info['Memory Percent']}%")
    root.after(1000, update_system_info_label)  # Schedule next update after 1 second

# Function to update process treeview widget
def update_process_tree():
    tree.delete(*tree.get_children())  # Clear existing entries in the treeview
    processes = get_running_processes()  # Get updated list of running processes
    for process in processes:
        # Insert process details into the treeview
        tree.insert('', 'end', values=(
            process['name'],
            process['pid'],  
            process['username'],
            f"{process['cpu_percent']}%",
            f"{process['memory_percent']}%"
        ))
    root.after(1000, update_process_tree)  # Schedule next update after 1 second

# Create main Tkinter window
root = tk.Tk()
root.title("System Monitor")

# Create label to display system information
system_info_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
system_info_label.pack(padx=20, pady=10)

# Create treeview widget to display running processes
tree = ttk.Treeview(root, columns=("Name", "PID", "Username", "CPU %", "Memory %"))
tree.heading("#1", text="Name")
tree.heading("#2", text="PID")
tree.heading("#3", text="Username")
tree.heading("#4", text="CPU %")
tree.heading("#5", text="Memory %")
tree.pack(fill="both", expand=True)

# Start updating system information and process treeview
update_system_info_label()
update_process_tree()

# Start Tkinter event loop
root.mainloop()